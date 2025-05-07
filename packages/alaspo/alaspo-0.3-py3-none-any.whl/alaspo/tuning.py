from __future__ import annotations

import hashlib
import importlib.util
import json
import logging
import os
import re
import subprocess
import sys
import time
import warnings
from collections import defaultdict
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from subprocess import CompletedProcess
from typing import Callable, NoReturn

import dask_jobqueue
import dill
import numpy as np
from ConfigSpace import Configuration, ConfigurationSpace
from dask.distributed import Client
from dask_jobqueue import *
from sklearn.cluster import KMeans
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from smac import Scenario, HyperparameterOptimizationFacade
from smac.initial_design import DefaultInitialDesign
from smac.intensifier.intensifier import Intensifier
from smac.main.config_selector import ConfigSelector
from smac.runhistory import TrialInfo, TrialValue, StatusType, RunHistory

from .tuning_util import setupLogger, ensureFilesExist, readFile, updateDictAtPath, deleteCondition, resolveConfigurationSpace, resolveRelativePath, findAlaspoExecutable, parseInstance, SimpleNumpyJsonEncoder, \
    visualizeClustering, default

logger = logging.getLogger(__name__)
setupLogger(logger)


class TuningConfig:
    def __init__(
            self,
            timeLimit: int | None,
            trials: int | None,
            trialTimeLimit: int,
            encoding: str | list[str],
            instances: str,
            configurationSpace: dict | ConfigurationSpace,
            defaultConfig: dict,
            *,
            alaspoClArgs: list[str] = None,
            clusterInstances: bool | None = None,
            clusterSize: int | None = None,
            passInstanceFeaturesToSmac: bool | None = None,
            customFeatureExtractor: Callable[[str], list[float]] | None = None,
            standardizeInstanceFeatures: bool | None = None,
            visualizeClustering: bool | None = None,
            outputDir: str | None = None,
            workingDir: str | None = None,
            daskCluster: JobQueueCluster | None = None,
            daskWorkers: int | None = None
    ):
        requiredKeys = {
            "`timeLimit` or `trials`": timeLimit or trials,
            "`trialTimeLimit`": trialTimeLimit,
            "`encoding`": encoding,
            "`instances`": instances,
            "`configurationSpace`": configurationSpace,
            "`defaultConfig`": defaultConfig,
            "both `daskCluster` and `daskWorkers` or neither": bool(daskCluster) == bool(daskWorkers)
        }
        if not all(requiredKeys.values()):
            raise Exception(f"Missing one or more required config parameter(s): {', '.join(requiredKeys.keys())}")

        if daskCluster and timeLimit:
            raise Exception("Do not use timeLimit when using daskCluster! Specify the number of trials!")

        self.timeLimit: int | None = timeLimit
        self.trials: int | None = trials
        self.trialTimeLimit: int = trialTimeLimit
        self.workingDir: str = workingDir or os.path.abspath(os.getcwd())
        self.encoding: str | list[str] = self.resolvePath(encoding) if isinstance(encoding, str) else [self.resolvePath(x) for x in encoding]
        ensureFilesExist(self.encoding)
        instances = self.resolvePath(instances)
        ensureFilesExist(instances)
        with open(instances, "r") as f:
            actualInstances = [resolveRelativePath(os.path.dirname(instances), x.strip("\n \r")) for x in f.readlines()]
            ensureFilesExist(actualInstances)
        self.instances: list[str] = actualInstances
        self.nonPrimitives, self.configurationSpace = resolveConfigurationSpace(configurationSpace)
        self.config: dict = defaultConfig
        self.alaspoClArgs: list[str] = default(alaspoClArgs, sys.argv[1:])
        self.clusterInstances: bool = default(clusterInstances, True)
        self.clusterSize: int | None = clusterSize
        self.passInstanceFeaturesToSmac: bool = default(passInstanceFeaturesToSmac, True)
        self.customFeatureExtractor: Callable[[str], list[float]] | None = customFeatureExtractor
        self.standardizeInstanceFeatures: bool = default(standardizeInstanceFeatures, True)
        self.visualizeClustering: bool = default(visualizeClustering, False)
        self.outputDir: str | None = outputDir
        self.instanceFeatures: list[str] = []
        self.daskCluster: JobQueueCluster | None = daskCluster
        self.daskWorkers: int | None = daskWorkers

    def resolvePath(self, path: str) -> str:
        return resolveRelativePath(self.workingDir, path)

    @staticmethod
    def fromConfigPath(configPath: str) -> TuningConfig:
        config: dict = dict(json.loads(readFile(configPath)))
        tuningConf: dict = config["tuning"]
        configDir = os.path.dirname(configPath)
        return TuningConfig(
            timeLimit=tuningConf.get("timeLimit"),
            trials=tuningConf.get("trials"),
            trialTimeLimit=tuningConf.get("trialTimeLimit"),
            encoding=tuningConf.get("encoding"),
            instances=tuningConf.get("instances"),
            configurationSpace=tuningConf.get("configurationSpace"),
            defaultConfig=config,
            alaspoClArgs=tuningConf.get("alaspoClArgs"),
            clusterInstances=tuningConf.get("clusterInstances"),
            clusterSize=tuningConf.get("clusterSize"),
            passInstanceFeaturesToSmac=tuningConf.get("passInstanceFeaturesToSmac"),
            customFeatureExtractor=TuningConfig.getCustomFeatureExtractorFromFile(resolveRelativePath(configDir, tuningConf.get("customFeatureExtractor"))),
            standardizeInstanceFeatures=tuningConf.get("standardizeInstanceFeatures"),
            visualizeClustering=tuningConf.get("visualizeClustering"),
            outputDir=tuningConf.get("outputDir"),
            workingDir=tuningConf.get("workingDir", configDir),
            daskCluster=(d := TuningConfig.parseDaskConfig(tuningConf.get("dask")))[0],
            daskWorkers=d[1]
        )

    @staticmethod
    def parseDaskConfig(daskConfig: dict) -> tuple[JobQueueCluster, int] | tuple[None, None]:
        if not daskConfig or not (clusterType := getattr(dask_jobqueue, daskConfig.pop("type", ""), False)):
            return None, None
        daskWorkers: int = daskConfig.pop("workers")
        cluster: JobQueueCluster = clusterType(**daskConfig)
        return cluster, daskWorkers

    @contextmanager
    def excludeDaskCluster(self):
        daskCluster = self.daskCluster
        self.daskCluster = None
        try:
            yield
        finally:
            self.daskCluster = daskCluster

    @staticmethod
    def getCustomFeatureExtractorFromFile(filePath: str) -> Callable[[str], list[float]] | None:
        if not filePath:
            return None
        ensureFilesExist(filePath)
        filePath = os.path.abspath(filePath)
        spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(filePath))[0], filePath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            return module.extractFeatures
        except AttributeError as e:
            raise Exception(f"No function named 'extractFeatures' found inside specified custom feature extractor at path '{filePath}'. "
                            "It has to have the signature 'extractFeatures(instancePath: str) -> list[float]'.") from e


###############################################################################################################################################################
###############################################################################################################################################################

class TunerFactory:
    @staticmethod
    def get(config: str | TuningConfig) -> ParameterTuner | DaskParameterTuner:
        c: TuningConfig = TuningConfig.fromConfigPath(config) if isinstance(config, str) else config
        if c.daskCluster:
            return DaskParameterTuner(c)
        return ParameterTuner(c)


###############################################################################################################################################################

class ParameterTuner:
    def __init__(self, config: str | TuningConfig):
        self.config: TuningConfig = TuningConfig.fromConfigPath(config) if isinstance(config, str) else config
        self.alaspoConfigs: dict[Configuration, dict[str, str]] = {}
        self.alaspoExecutable: str = findAlaspoExecutable()
        self.directory: str = self.config.outputDir or f"./tuning_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        os.makedirs(f"{self.directory}/alaspoConfigs/", exist_ok=True)
        self.results: dict[str, dict[str, float | None]] = defaultdict(lambda: defaultdict(lambda: None))

    def extractFeatures(self, instance: str) -> list[float]:  # does not handle e.g. clingo-dl - &diff directives (should be fine? since its instances; also, a custom extractor can be used)
        if self.config.customFeatureExtractor:
            res = self.config.customFeatureExtractor(instance)
            if not isinstance(res, list) or not all([isinstance(x, (float, int)) for x in res]):
                raise Exception(f"Custom feature extractor does not return list[float]. It returned {type(res)}: {res} instead.")
            return res
        counts: defaultdict = parseInstance(instance)
        if not self.config.instanceFeatures:  # take the features of first instance
            self.config.instanceFeatures = counts.keys()
        return [counts.get(f, 0) for f in self.config.instanceFeatures]

    @staticmethod
    def parseOutput(output: str) -> float:
        cost = None
        for line in output.splitlines():
            if "Cost" in line:
                c = line.split("Cost: ")[1]
                if c == "None":
                    continue
                cost = float(c)
        return cost if cost is not None else float('inf')

    def getAlaspoConfig(self, configuration: Configuration) -> str:
        if configuration in self.alaspoConfigs.keys():
            return self.alaspoConfigs[configuration]["path"]

        alaspoConfig = self.generateConfig(configuration)
        jsonDumps = json.dumps(alaspoConfig, indent=2, cls=SimpleNumpyJsonEncoder)
        path = os.path.join(self.directory, "alaspoConfigs", hashlib.sha256(jsonDumps.encode()).hexdigest() + ".json")

        with open(path, "w") as f:
            f.write(jsonDumps)
        self.alaspoConfigs[configuration] = {"path": path, "config": json.dumps(alaspoConfig, cls=SimpleNumpyJsonEncoder, separators=(",", ":"))}
        return path

    def generateConfig(self, configuration: Configuration) -> dict:
        alaspoConfig: dict = deepcopy(self.config.config)
        if "tuning" in alaspoConfig:
            del alaspoConfig["tuning"]
        for condition in configuration.config_space.conditions:
            deleteCondition(alaspoConfig, condition)  # cleanup conditional parameters (that may be contained in user-provided configuration)
        for k, v in configuration.items():
            v = self.config.nonPrimitives.get(v, v)  # resolve non-primitive types
            updateDictAtPath(k, v, alaspoConfig)
        return alaspoConfig

    def callAlaspo(self, configuration: Configuration, seed: int, instance: str) -> float:
        args = [x for arg in self.config.alaspoClArgs for x in (arg.split('=', 1) if '=' in arg else [arg])]
        if "--tuning-config" in args:
            idx = args.index("--tuning-config")
            args.pop(idx)
            args.pop(idx)

        alaspoConfig = self.getAlaspoConfig(configuration)
        cmd = f"{self.alaspoExecutable} {' '.join(args)} --seed {seed} --time-limit {self.config.trialTimeLimit} -c {alaspoConfig} -i {' '.join(self.config.encoding) if isinstance(self.config.encoding, list) else self.config.encoding} {instance}"
        logger.info(f"{configuration._values} - {instance}")
        process: CompletedProcess = subprocess.run(
            re.split("\s+|=", cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        cost = self.parseOutput(process.stdout)
        logger.info(f"Cost: {cost}")
        self.results[instance][alaspoConfig] = cost
        return cost

    @staticmethod
    def kMeans(n_clusters: int, values: list[list[float]]) -> tuple[list[int], KMeans]:
        estimator: KMeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42).fit(values)
        return estimator.predict(values), estimator

    def clusterInstances(self, featureMap: dict[str, list[float]]) -> dict[int, list[str]]:
        features = list(featureMap.values())
        instances = featureMap.keys()

        if not self.config.clusterInstances or len(instances) <= 2:
            with self.config.excludeDaskCluster():
                with open(os.path.join(self.directory, "clustering.dill"), "ab") as f:
                    dill.dump(None, f)
            return {0: self.config.instances}

        if self.config.clusterSize:
            labels, estimator = self.kMeans(self.config.clusterSize, features)
        else:  # use silhouette score to determine the best cluster size
            bestScore = -2
            warnings.filterwarnings(action="error", category=ConvergenceWarning)
            for i in range(2, len(instances)):
                try:
                    labels_, estimator_ = self.kMeans(i, features)
                except ConvergenceWarning:
                    break
                score = silhouette_score(features, labels_)
                if score > bestScore:
                    bestScore = score
                    labels = labels_
                    estimator = estimator_

        with self.config.excludeDaskCluster():
            with open(os.path.join(self.directory, "clustering.dill"), "ab") as f:
                dill.dump(estimator, f)

        clusters = defaultdict(list)
        for cluster, instance in zip(labels, instances):
            clusters[int(cluster)].append(instance)

        logger.info(f"Determined best number of clusters: {max(clusters.keys()) + 1}")
        return clusters

    @staticmethod
    def splitSimpleBudget(budget: int, clusters: int, clusterInstances: int, allInstances: int) -> float:
        return ((budget * 0.5) / clusters) + ((budget * 0.5 * clusterInstances) / allInstances)

    @staticmethod
    def splitTimeBudget(budget: int, clusters: dict[int, list[str]], allInstances: int) -> dict[int, float]:
        if not budget:
            return {c: np.inf for c in clusters.keys()}
        return {c: ParameterTuner.splitSimpleBudget(budget, len(clusters), len(i), allInstances) for c, i in clusters.items()}

    @staticmethod
    def splitTrialsBudget(budget: int, clusters: dict[int, list[str]], allInstances: int) -> dict[int, int]:
        if not budget:
            return {c: np.inf for c in clusters.keys()}
        trialsBudgetMap: dict[int, int] = {c: int(ParameterTuner.splitSimpleBudget(budget, len(clusters), len(i), allInstances)) for c, i in clusters.items()}
        diff: int = budget - sum(trialsBudgetMap.values())  # remaining trials lost due to truncation
        for cluster in sorted(clusters.keys(), key=lambda c: len(clusters[c]), reverse=True)[:diff]:
            trialsBudgetMap[cluster] += 1
        return trialsBudgetMap

    def tune(self) -> NoReturn:
        logger.info(f'Starting Hyperparameter Tuning')

        instanceFeatures: dict[str, list[float]] = {x: self.extractFeatures(x) for x in self.config.instances}
        scaler = None
        if self.config.standardizeInstanceFeatures:
            scaler = StandardScaler()
            standardizedFeatures = scaler.fit_transform(list(instanceFeatures.values())).tolist()
            instanceFeatures = dict(zip(instanceFeatures.keys(), standardizedFeatures))
        with self.config.excludeDaskCluster():
            with open(os.path.join(self.directory, "clustering.dill"), "wb") as f:
                dill.dump(scaler, f)
                dill.dump(self.extractFeatures, f)
        clusters: dict[int, list[str]] = self.clusterInstances(instanceFeatures)
        if self.config.visualizeClustering:
            visualizeClustering(
                clusterFeatures={k: [instanceFeatures[x] for x in v] for k, v in clusters.items()},
                clusterInstanceNames={k: [os.path.basename(x) for x in v] for k, v in clusters.items()},
                outputDir=self.directory
            )

        outFile: dict = {k: {"instances": v} for k, v in clusters.items()}

        timeBudgets: dict[int, float] = self.splitTimeBudget(self.config.timeLimit, clusters, len(self.config.instances))
        trialsBudgets: dict[int, int] = self.splitTrialsBudget(self.config.trials, clusters, len(self.config.instances))

        self.mainLoop(clusters, instanceFeatures, outFile, timeBudgets, trialsBudgets)

        with self.config.excludeDaskCluster():
            with open(os.path.join(self.directory, "clustering.dill"), "ab") as f:
                dill.dump(outFile, f)

        with open(os.path.join(self.directory, "results.json"), "w") as f:
            json.dump(outFile, f, indent=2, sort_keys=True)

        self.createCSV()

        logger.info(f"Finished tuning! Results written to {self.directory}")
        exit(0)

    def createCSV(self) -> None:
        with open(os.path.join(self.directory, "results.csv"), "w") as f:
            configPaths = [x["path"] for x in self.alaspoConfigs.values()]
            s = f"instance, {', '.join(configPaths)}\n"
            for instance, costMap in self.results.items():
                s += f"{instance},  {', '.join([str(costMap[config]) for config in configPaths])}\n"
            f.write(s)

    def mainLoop(self, clusters: dict[int, list[str]], instanceFeatures: dict[str, list[float]], outFile: dict, timeBudgets: dict[int, float], trialsBudgets: dict[int, int]) -> None:
        for cluster, instances in clusters.items():
            logger.info(f"Tuning cluster {cluster}")

            incumbent: Configuration = self.runSmac(timeBudgets[cluster], trialsBudgets[cluster], instances, {k: v for k, v in instanceFeatures.items() if k in instances})

            if not incumbent:  # too little time specified no experiment was run for this cluster
                raise Exception(f"The *timeLimit* specified is too little! Aborting!")

            bestConfig = self.alaspoConfigs[incumbent]
            outFile[cluster].update(bestConfig)
            logger.info(f"Best configuration for cluster {cluster}: {bestConfig['path']}")

    def runSmac(self, timeLimit: float, trialLimit: int, instances: list[str], instanceFeatures: dict[str, list[float]]) -> Configuration:
        scenario = Scenario(
            self.config.configurationSpace,
            deterministic=False,
            walltime_limit=timeLimit,
            n_trials=trialLimit,
            instances=instances,
            instance_features=instanceFeatures if self.config.passInstanceFeaturesToSmac else {instance: [i] for i, instance in enumerate(instances)},
            output_directory=Path(os.path.join(self.directory, "smac3_output"))
        )
        intensifier = Intensifier(scenario, max_config_calls=len(instances) * 5)  # set max_config_calls to make smac test on as many instances as it can (not just 3 by default) *with max 5 seeds per instance*
        initialDesign = DefaultInitialDesign(scenario)
        configSelector = ConfigSelector(scenario, retries=999)
        smac = HyperparameterOptimizationFacade(scenario, self.callAlaspo, intensifier=intensifier, initial_design=initialDesign, config_selector=configSelector)
        scenarioStartTime = time.time()
        trials = 0
        timeLimit: Callable[[], bool] = lambda: scenario.walltime_limit - (time.time() - scenarioStartTime) <= self.config.trialTimeLimit
        trialLimit: Callable[[], bool] = lambda: trials >= scenario.n_trials
        smacStop: Callable[[], bool] = lambda: (timeLimit() if self.config.timeLimit else False) or (trialLimit() if self.config.trials else False)
        while not smacStop():
            try:
                info: TrialInfo = smac.ask()
            except StopIteration:
                logger.info("No new configuration found to test.")
                break
            trialStartTime = time.time()
            cost = self.callAlaspo(info.config, info.seed, info.instance)
            trialEndTime = time.time()
            success: bool = cost is not None and not cost == float('inf')
            smac.tell(info, TrialValue(cost=cost, time=trialEndTime - trialStartTime, starttime=trialStartTime, endtime=trialEndTime, status=StatusType.SUCCESS if success else StatusType.CRASHED))
            trials += 1
        return smac.intensifier.get_incumbent()


###############################################################################################################################################################

class DaskParameterTuner(ParameterTuner):
    def mainLoop(self, clusters: dict[int, list[str]], instanceFeatures: dict[str, list[float]], outFile: dict, timeBudgets: dict[int, float], trialsBudgets: dict[int, int]) -> None:
        try:
            daskCluster: JobQueueCluster = self.config.daskCluster
            self.config.daskCluster = None  # remove unserializable object
            daskCluster.scale(self.config.daskWorkers)
            daskClient = Client(daskCluster)

            for cluster, instances in clusters.items():
                logger.info(f"Tuning cluster {cluster}")

                daskClient.wait_for_workers(1)  # wait until atleast one worker is ready
                incumbent: Configuration = self.runSmac(timeBudgets[cluster], trialsBudgets[cluster], instances, {k: v for k, v in instanceFeatures.items() if k in instances}, daskClient)

                if not incumbent:  # too little time specified no experiment was run for this cluster
                    raise Exception(f"The *timeLimit* specified is too little! Aborting!")

                bestConfig = {"path": (p := self.getAlaspoConfig(incumbent)), "config": readFile(p)}
                outFile[cluster].update(bestConfig)
                logger.info(f"Best configuration for cluster {cluster}: {bestConfig['path']}")
        finally:
            daskClient.shutdown()

    def runSmac(self, timeLimit: float, trialLimit: int, instances: list[str], instanceFeatures: dict[str, list[float]], daskClient: Client = None) -> Configuration:
        scenario = Scenario(
            self.config.configurationSpace,
            deterministic=False,
            walltime_limit=timeLimit,
            n_trials=trialLimit,
            instances=instances,
            instance_features=instanceFeatures if self.config.passInstanceFeaturesToSmac else {instance: [i] for i, instance in enumerate(instances)},
            output_directory=Path(os.path.join(self.directory, "smac3_output"))
        )
        intensifier = Intensifier(scenario, max_config_calls=len(instances) * 5)  # set max_config_calls to make smac test on as many instances as it can (not just 3 by default) *with max 5 seeds per instance*
        initialDesign = DefaultInitialDesign(scenario)
        configSelector = ConfigSelector(scenario, retries=999)
        smac = HyperparameterOptimizationFacade(scenario, self.callAlaspo, intensifier=intensifier, initial_design=initialDesign, dask_client=daskClient, config_selector=configSelector)
        incumbent: Configuration = smac.optimize()
        return incumbent

    def createCSV(self) -> None:
        if not os.path.exists(smacOutputDir := os.path.join(self.directory, "smac3_output")):
            return
        logger.info("Creating CSV file from SMAC3 runhistory ...")
        totalRh: RunHistory = RunHistory()
        for rhPath in Path(smacOutputDir).rglob("runhistory.json"):
            totalRh.update_from_json(rhPath, self.config.configurationSpace)
        self.alaspoConfigs = {c: {"path": self.getAlaspoConfig(c)} for c in totalRh.get_configs()}
        for k, v in totalRh.items():
            conf = totalRh.get_config(k.config_id)
            self.results[k.instance][self.alaspoConfigs[conf]["path"]] = v.cost
        super().createCSV()
