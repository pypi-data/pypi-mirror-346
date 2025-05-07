import random
import sys
import os
import argparse
import signal
import logging
from . import lns
from . import solver
from . import initial
from . import strategy
from . import json_config
from . import relax
from . import search
from .__version__ import __version__
from .__init__ import logger

verbose = 0


def print_model(model):
    for a in model.shown:
        print(a, end=' ')
    print(" ")


def print_solution(solution, complete):
    if solution != None:
        if complete:
            print("Optimal solution:")
        else:
            print("Best found solution:")
        print_model(solution.model)
        print(f"Cost: {solution.cost}")
    else:
        print("No solution found")


def on_solution(solution, time):
    global verbose
    if verbose > 1:
        print('Solution:')
        print_model(solution.model)
        print(f'Time: {round(time, 3)}s')
    if verbose > 0:
        print(f'Cost: {solution.cost}')


def main():
    def existing_files(argument):
        if os.path.exists(argument) and os.path.isfile(argument):
            return argument
        else:
            raise argparse.ArgumentTypeError('File not found!')

    def valid_quick_config(argument):
        conf = argument.split(',')
        if len(conf) != 3:
            raise argparse.ArgumentTypeError('config string is not correct!')
        rate = float(conf[1])
        if not (0 <= rate <= 1):
            raise argparse.ArgumentTypeError('0 <= rate <= 1 required!')

        time = int(conf[2])
        if not (0 < time):
            raise argparse.ArgumentTypeError('timeout > 0 required!')

        return argument

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=f'ALASPO: ASP + Large-Neighborhood Search (version {__version__})')

    parser.add_argument('-i', '--input', type=existing_files, metavar='file', default=None, nargs='+',
                        help='input ASP files')

    parser.add_argument('-gt', '--time-limit', type=int, metavar='<n>', default=300,
                        help='time limit for the lns search')

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-c", "--config-file", type=existing_files, metavar='<file>',
                       help='the config file specifying the relax and search operators')

    group.add_argument("-q", "--quick-config", type=valid_quick_config, metavar='<config>',
                       help='a config string containing a neighborhood type ("randomAtoms", "randomConstaints" or "declarative"), a relaxation rate, and a move timeout seperated by comma')

    tuning_group = parser.add_argument_group("tuning")
    tuning_group.add_argument("--tuning-config", type=existing_files, metavar='<config>',
                              help='the config file specifying the parameter tuning approach; for tuning documentation read examples/tuning/README.md')
    tuning_group.add_argument("--use-clustering", type=existing_files, metavar='<clustering.dill>',
                              help='the clustering.dill file specifying the the best configuration files per instance-cluster, resulting from a previous tuning run. Requires the use of "--instance"')
    tuning_group.add_argument('--instance', type=existing_files, metavar='<instance>',
                              help='the instance file which will determine the best configuration to be used. It will also be used as input ASP file')

    parser.add_argument('-st', '--solver-type', type=str, choices=['clingo', 'clingo-dl', 'clingcon'],
                        metavar='<arg>', default='clingo',
                        help='the ASP solver ("clingo", "clingo-dl", "clingcon") to be used')

    parser.add_argument('-mv', '--minimize-variable', type=str, metavar='<var>', default=None,
                        help='an integer variable to minimize (only useful with solver type "clingo-dl")')

    parser.add_argument('-sd', '--seed', type=int, metavar='SEED', default=None,
                        help='seed for random numbers')

    parser.add_argument('-ia', '--interactive', action='store_true',
                        help='select interactive selection strategy')
    parser.set_defaults(interactive=False)

    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
                        metavar='<level>', default=1,
                        help='the level of verbosity in the output: 0 only output best found solution, 1 for updates about the incumbent cost, 2 for intermediate solutions')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug logging')
    parser.set_defaults(debug=False)

    args = parser.parse_args()

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    global verbose
    verbose = args.verbosity

    if args.tuning_config:
        from . import tuning
        tuning.TunerFactory.get(args.tuning_config).tune()

    if args.use_clustering:
        if not args.instance:
            raise Exception('No instance file specified. Use "--instance" to specify the instance file.')
        if not args.input or not args.instance in args.input:
            args.input = (args.input or []) + [args.instance]

    if args.debug:
        logger.setLevel(level=logging.DEBUG)

    if args.seed is None:
        seed_value = random.randrange(sys.maxsize)
    else:
        seed_value = args.seed

    logger.info(f'Seed: {seed_value}')

    if verbose > 0:
        print(f'Seed: {seed_value}')

    random.seed(seed_value)

    program = ''
    if args.input is not None:
        for asp_file in args.input:
            with open(asp_file, 'r') as f:
                program += f.read()
    else:
        program += sys.stdin.read()

    internal_solver = None
    if args.solver_type == 'clingo':
        internal_solver = solver.Clingo(seed=seed_value)
    elif args.solver_type == 'clingo-dl':
        internal_solver = solver.ClingoDl(
            minimize_variable=args.minimize_variable, seed=seed_value)
    elif args.solver_type == 'clingcon':
        internal_solver = solver.Clingcon(seed=seed_value)
    else:
        raise ValueError("Not a valid solver type!")

    strat = None
    initial_operator = None
    relax_operators = None
    search_operators = None

    if args.config_file != None:
        with open(args.config_file, 'r') as f:
            con = f.read()
            strat, initial_operator, relax_operators, search_operators = json_config.parse_config(
                con, internal_solver)
    elif args.quick_config != None:
        conf_string = args.quick_config.split(',')
        op_name = conf_string[0].strip()
        rate = float(conf_string[1].strip())
        mt = int(conf_string[2].strip())

        strat = strategy.RandomStrategy(supports_intensification=True)
        relax_operators = [relax.get_operator(op_name, {'sizes': [rate]})]
        search_operators = [search.get_operator(
            'default', {'timeouts': [mt]}, internal_solver)]
    elif args.use_clustering:
        import dill
        with open(args.use_clustering, "rb") as f:
            scaler = dill.load(f)
            extractFeatures = dill.load(f)
            estimator = dill.load(f)
            configs = dill.load(f)
            if estimator:
                features = [extractFeatures(args.instance)]
                if scaler:
                    features = scaler.transform(features)
                cluster = estimator.predict(features)[0]
                bestConfig = configs[cluster]["config"]
                logger.info(f"Predicted instance to belong to cluster {cluster}")
            else:
                bestConfig = configs[0]["config"]
            logger.info(f"Determined the best configuration to be: {bestConfig}")
            strat, initial_operator, relax_operators, search_operators = json_config.parse_config(
                bestConfig, internal_solver)
    else:
        strat, initial_operator, relax_operators, search_operators = json_config.parse_config(
            json_config.DEFAULT_CONFIG, internal_solver)

    if initial_operator == None:
        initial_operator = initial.ClingoInitialOperator(internal_solver)

    # for interactive mode
    if args.interactive is True:
        strat = strategy.InteractiveStrategy()

    print('Solving...')
    lns_solver = lns.ClingoLNS(
        internal_solver, program, initial_operator, relax_operators, search_operators, strat)

    def signal_handler(sig, _):
        nonlocal lns_solver, strat
        sys.stderr.flush()
        sys.stdout.flush()
        print(f'Search interrupted! ({sig})')
        if verbose > 0:
            print_solution(lns_solver.best_solution,
                           lns_solver.search_complete)

        if sig != signal.SIGTERM and type(strat) == strategy.InteractiveStrategy:
            search_op = lns_solver.search_operator
            relax_op = lns_solver.relax_operator
            relax_operators, search_operators = lns_solver.get_portfolio()
            print(f'Current search configuration: {search_op.name()}')
            print('Search portfolio:')
            for i in range(len(search_operators)):
                print(f'{i}: {search_operators[i].name()}')
            while True:
                search = input(
                    'Select search configuration (ENTER = no change, C = exit): ')
                if search == '':
                    break
                if search.upper() == 'C':
                    sys.exit(0)
                if search.isdigit():
                    search_index = int(search)
                    if 0 <= search_index < len(search_operators):
                        search_op = search_operators[search_index]
                        break
                print('Not a valid index!')

            print(f'Current neighbourhood: {relax_op.name()}')
            print('Neighbourhood portfolio:')
            for i in range(len(relax_operators)):
                print(f'{i}: {relax_operators[i].name()}')
            while True:
                nh = input(
                    'Select search configuration (ENTER = no change, C = exit): ')
                if nh == '':
                    break
                if nh.upper() == 'C':
                    sys.exit(0)
                if nh.isdigit():
                    nh_index = int(nh)
                    if 0 <= nh_index < len(relax_operators):
                        relax_op = relax_operators[nh_index]
                        break
                print('Not a valid index!')

            strat.set_operators(relax_op, search_op)
        else:
            sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    solution = lns_solver.solve(args.time_limit, on_solution=on_solution)
    if verbose < 2:
        print_solution(solution, lns_solver.search_complete)
    elif lns_solver.search_complete:
        print('Found optimal solution.')


if __name__ == '__main__':
    main()
