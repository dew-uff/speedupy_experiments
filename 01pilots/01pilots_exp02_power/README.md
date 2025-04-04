# Power Experiment

## Experiment dependencies
This experiment has no dependencies.

To run the experiment, make sure you have the appropriate release of SpeeduPy installed. Instructions on which release to use and how to install it can be found [here](https://github.com/dew-uff/memoization/blob/main/README.md#reproducing-the-article-analyses). Ensure that the **speedupy/** folder is located in the same directory as the main experiment script.

## Trials Used in the Article
The five trials used on the memoization techniques article use the same script **power.py** with the following inputs:

- **1241231241 462**
- **1241231241 450**
- **1241231000 430**
- **124123124 400**
- **1241231231 460**

To execute a trial, type:

```bash
python speedupy/setup_exp/setup.py power.py
python power.py 1241231231 460 --exec-mode manual
```
