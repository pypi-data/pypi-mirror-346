# ALASPO

An (adaptive) LNS framework for the for ASP systems. Currently, the system only supports solvers based on [clingo](https://potassco.org/). 

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

Examples for portfolio config files can be found in the [git repository](https://gitlab.tuwien.ac.at/kbs/BAI/alaspo).
