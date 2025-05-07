
import json
from . import strategy
from . import relax
from . import search
from . import initial

DEFAULT_CONFIG = """
{
    "strategy": {
        "name": "dynamic",
        "unsatStrikes": 3,
        "timeoutStrikes": 1
    },
    "relaxOperators": [
        {
            "type": "randomAtoms",
            "sizes": [ 0.1, 0.2, 0.4, 0.6, 0.8 ]
        },
        {
            "type": "randomConstants",
            "sizes": [ 0.1, 0.2, 0.3, 0.5 ]
        }
    ],
    "searchOperators": [
        {
            "name": "default",
            "timeouts": [ 5, 15, 30, 60 ]
        }
    ]
}
"""


def parse_config(config, internal_solver):
    json_config = json.loads(config)

    json_strategy = json_config['strategy']
    strat_name = json_strategy['name']
    strat_args = {k: v for k, v in json_strategy.items() if k != 'name'}

    strategy_op = strategy.get_strategy(strat_name, strat_args)

    relax_operators = []
    for json_relax in json_config['relaxOperators']:
        relax_type = json_relax['type']
        relax_args = {k: v for k, v in json_relax.items() if k != 'type'}
        relax_operators += [relax.get_operator(relax_type, relax_args)]

    search_operators = []
    for json_search in json_config['searchOperators']:
        search_name = json_search['name']
        search_args = {k: v for k, v in json_search.items() if k != 'type'}
        search_operators += [search.get_operator(
            search_name, search_args, internal_solver)]

    initial_operator = None
    if 'initialOperator' in json_config:
        json_initial = json_config['initialOperator']
        initial_args = {k: v for k, v in json_initial.items()}
        initial_operator = initial.get_operator(initial_args, internal_solver)

    return strategy_op, initial_operator, relax_operators, search_operators
