from __future__ import annotations

import ast
import hashlib
import json
import logging
import os
import re
import shutil
import sys
from collections import defaultdict
from typing import TypeVar

import ConfigSpace
import numpy as np
from ConfigSpace import ConfigurationSpace
from clingo.ast import Transformer, AST, parse_files
from jsonpath_ng import JSONPath, parse

from .json_config import DEFAULT_CONFIG


def setupLogger(logger: logging.Logger) -> None:
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False


def addDupPrefix(s: str, count: int) -> str:
    return f"#{count}_" + s


def removeDupPrefix(s: str) -> str:  # remove potential prefix that was added to avoid name conflicts (e.g., two strategies with equally named parameters)
    if not s.startswith("#"):
        return s
    return re.sub("^#\d+_", "", s)


class CfgPreproc:
    evalPrefix: str = "$eval:"

    @staticmethod
    def resolvePrefixes(item: dict | list) -> None:
        if isinstance(item, dict):
            CfgPreproc._resolveDict(item)
        elif isinstance(item, list):
            CfgPreproc._resolveList(item)

    @staticmethod
    def _resolveDict(dict_: dict) -> None:
        for key, val in dict_.items():
            dict_[key] = CfgPreproc._evalStringIfPrefixed(val)
            CfgPreproc.resolvePrefixes(dict_[key])

    @staticmethod
    def _resolveList(list_: list) -> None:
        for i, x in enumerate(list_):
            list_[i] = CfgPreproc._evalStringIfPrefixed(x)
            CfgPreproc.resolvePrefixes(list_[i])

    @staticmethod
    def _evalStringIfPrefixed(s: str | any) -> str | any:
        if isinstance(s, str) and s.startswith(CfgPreproc.evalPrefix):
            # return eval(s[len(self.evalPrefix):])
            return ast.literal_eval(s[len(CfgPreproc.evalPrefix):])
        return s

    @staticmethod
    def resolveNonPrimitives(dict_: dict) -> dict[str, object]:
        nonPrimitives: dict[str, object] = dict()
        for key, val in dict_.items():
            if not isinstance(val, list) or key == "strategy":
                continue
            for i, x in enumerate(val):
                if not isPrimitive(x):
                    hexdigest = sha256_hexdigest(str(x))
                    nonPrimitives[hexdigest] = x
                    val[i] = hexdigest
        return nonPrimitives


def isPrimitive(obj: any) -> bool:
    return isinstance(obj, (int, float, str, bool, type(None)))


def sha256_hexdigest(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def ConfigurationSpace_withDefaults(space: dict) -> ConfigurationSpace:  # set defaults for provided hyperparameters IF the default is valid
    defaultConfig = json.loads(DEFAULT_CONFIG)
    hyperparameters = list(ConfigurationSpace(space).values())

    for hp in hyperparameters:
        if d := parse(removeDupPrefix(hp.name)).find(defaultConfig):
            dVal = d[0].value
            if not isPrimitive(dVal):
                dVal = sha256_hexdigest(str(dVal))

            if hp.legal_value(dVal):  # i.e., check if the default value is either (1) within the provided choices for categorical hps or (2) inside the range of a uniform hp
                hp.default_value = dVal

    return ConfigurationSpace(hyperparameters)


def resolveConfigurationSpace(configConfigurationSpace: dict | ConfigurationSpace | None) -> tuple[dict[str, object], ConfigurationSpace]:
    if isinstance(configConfigurationSpace, ConfigurationSpace):
        return {}, configConfigurationSpace

    CfgPreproc.resolvePrefixes(configConfigurationSpace)
    nonPrimitives: dict[str, object] = CfgPreproc.resolveNonPrimitives(configConfigurationSpace)

    # resolve conditional parameters of strategies
    strategySelection: list[dict] = [s] if not isinstance(s := configConfigurationSpace.pop("strategy", []), list) else s
    if not strategySelection:
        return nonPrimitives, ConfigurationSpace_withDefaults(configConfigurationSpace)

    space = {"strategy.name": []}
    if configConfigurationSpace:
        space = {**space, **configConfigurationSpace}

    prefixCounts: dict[str, int] = defaultdict(lambda: 2)  # keep track of the number of occurrences of duplicate conditional parameters
    conditions: list[tuple[str, str, str]] = []
    for strat in strategySelection:
        stratName = strat["name"]
        space["strategy.name"].append(stratName)
        for k, v in strat.items():
            if k != "name":
                conditional = f"strategy.{k}"
                if conditional in space:  # equally named conditional hyperparameter exists
                    count = prefixCounts[conditional]
                    prefixCounts[conditional] += 1
                    conditional = addDupPrefix(conditional, count)
                space[conditional] = v
                conditions.append((conditional, "strategy.name", stratName))  # set ´conditional´ hyperparameter active if the value of the ´strategy.name´ hyperparameter equals ´stratName´

    cs = ConfigurationSpace_withDefaults(space)
    cs.add([ConfigSpace.conditions.EqualsCondition(cs[option], cs[strategy], strategyName) for option, strategy, strategyName in conditions])
    return nonPrimitives, cs


def updateDictAtPath(jsonPath: str, value, config: dict) -> None:
    path: JSONPath = parse(removeDupPrefix(jsonPath))
    path.update_or_create(config, value)


def deleteCondition(alaspoConfig: dict, condition: ConfigSpace.conditions.AbstractCondition) -> None:
    path: JSONPath = parse(removeDupPrefix(condition.child.name))
    path.filter(lambda _: True, alaspoConfig)


T = TypeVar('T')
U = TypeVar('U')


def default(obj: T | None, default: U) -> T | U:
    return obj if obj is not None else default


def readFile(filePath: str) -> str:
    with open(filePath, "r") as f:
        return f.read()


def ensureFilesExist(path_s: str | list[str]) -> None:
    if isinstance(path_s, str):
        path_s = [path_s]
    for path in path_s:
        if not os.path.exists(path) or os.path.isdir(path):
            raise FileNotFoundError(f"{path}")


def resolveRelativePath(directory: str, path: str) -> str | None:
    if path is None or os.path.isabs(path) or path.startswith("~"):
        return path
    return os.path.abspath(os.path.join(directory, path))


def findAlaspoExecutable() -> str:
    alaspoPath: str
    if os.name == 'nt':  # Windows
        alaspoPath = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'alaspo.exe')
    else:
        alaspoPath = os.path.join(os.path.dirname(sys.executable), 'alaspo')

    if not os.path.exists(alaspoPath):  # not in env -> check PATH
        alaspoPath = shutil.which("alaspo")
        if not alaspoPath:
            return "alaspo"
    return alaspoPath


class AstVisitor(Transformer):
    def __init__(self):
        self.symbolicAtoms = defaultdict(lambda: 0)

    def visit_SymbolicAtom(self, ast: AST) -> AST:
        self.symbolicAtoms[ast.symbol.name] += 1
        return ast


def parseInstance(path: str) -> defaultdict:
    visitor = AstVisitor()
    parse_files([path], lambda stm: visitor(stm))
    return visitor.symbolicAtoms


class SimpleNumpyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        elif isinstance(o, np.bool_):
            return bool(o)
        return super().default(o)


def visualizeClustering(clusterFeatures: dict[int, list[list[float]]], clusterInstanceNames: dict[int, list[str]], outputDir: str) -> None:
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    import plotly.express as px

    labels, features, hoverInstanceNames = [], [], []

    for label, featuresList in clusterFeatures.items():
        features.extend(featuresList)
        labels.extend([label] * len(featuresList))
        hoverInstanceNames.extend(clusterInstanceNames[label])

    labels = np.array(labels)
    pcaFeatures_3d = PCA(n_components=3).fit_transform(features)
    pcaFeatures_2d = pcaFeatures_3d[:, :2]

    for label in clusterFeatures.keys():
        indices = labels == label
        plt.scatter(pcaFeatures_2d[indices, 0], pcaFeatures_2d[indices, 1], label=f'Cluster {label}')
    plt.title('Instance Clustering')
    plt.xlabel('PCA-1')
    plt.ylabel('PCA-2')
    plt.legend()
    plt.savefig(os.path.join(outputDir, 'clustering_plot_2d.pdf'))

    fig = px.scatter_3d(
        x=pcaFeatures_3d[:, 0],
        y=pcaFeatures_3d[:, 1],
        z=pcaFeatures_3d[:, 2],
        hover_name=hoverInstanceNames,
        color=labels.astype(str),
        title="Interactive Instance Clustering",
        labels={"x": "PCA-1", "y": "PCA-2", "z": "PCA-3", "color": "Cluster"}
    )
    fig.write_html(file=os.path.join(outputDir, "clustering_plot_3d.html"), include_plotlyjs=True)
