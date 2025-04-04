# Eq Solver Experiment

## Experiment dependencies
This experiment has the following dependencies: **numpy, scipy**

To install them, execute: **pip install numpy scipy**

To run the experiment, make sure you have the appropriate release of SpeeduPy installed. Instructions on which release to use and how to install it can be found [here](https://github.com/dew-uff/memoization/blob/main/README.md#reproducing-the-article-analyses). Ensure that the **speedupy/** folder is located in the same directory as the main experiment script.

## Trials Used in the Article
The five trials used on the memoization techniques article are:

- eq_solver_speedupy_1.py
- eq_solver_speedupy_2.py
- eq_solver_speedupy_3.py
- eq_solver_speedupy_4.py
- eq_solver_speedupy.py

To execute a trial, type:

```bash
python speedupy/setup_exp/setup.py SCRIPT_NAME.py
python SCRIPT_NAME.py 1000 --exec-mode manual
```
