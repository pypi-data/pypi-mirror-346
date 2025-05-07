# ALASPO

An (adaptive) LNS framework for the for ASP systems. Currently, the system only supports solvers based on [clingo](https://potassco.org/). 

The folder `src/alaspo` contains the LNS implementation as well as simple problem-independent relaxation operators and adaption strategies. 

## Installation

It should work out-of-the-box in a conda env after running the following commands:
```
conda create -n alaspo python=3.9
conda activate alaspo
conda install -c potassco clingo clingo-dl clingcon
python -m pip install alaspo
```

The command-line options of the problem-independent LNS can be shown as follows:
```
alaspo -h
```

Examples for portfolio config files can be found in the `examples` folder.

## Development

You can also clone the repository an run alaspo without installing the module:
```
git clone https://gitlab.tuwien.ac.at/kbs/BAI/alaspo.git
cd alaspo/src
python -m alaspo -h
```

## Tuning

To find good performing configurations, [SMAC3](https://github.com/automl/SMAC3) has been integrated to allow tuning different parts of the alaspo configuration.
For documentation see [Tuning README](./examples/tuning/README.md).

## Licencse

This software is distributed under the [MIT License](./LICENSE).
