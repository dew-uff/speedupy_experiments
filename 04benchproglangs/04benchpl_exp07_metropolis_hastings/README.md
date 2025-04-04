# Metropolis Hastings Experiment

## Experiment dependencies
This experiment has the following dependency: numpy

To install it, execute: **pip install numpy**

To run the experiment, make sure you have the appropriate release of SpeeduPy installed. Instructions on which release to use and how to install it can be found [here](https://github.com/dew-uff/memoization/blob/main/README.md#reproducing-the-article-analyses). Ensure that the **speedupy/** folder is located in the same directory as the main experiment script.

## Trials Used in the Article
The five trials used on the memoization techniques article use the same script **metropolis_hastings.py** with the following inputs:

- **75000**
- **72500**
- **70000**
- **67500**
- **65000**

To execute a trial, type:

```bash
python speedupy/setup_exp/setup.py metropolis_hastings.py
python metropolis_hastings.py 65000 --exec-mode manual
```
