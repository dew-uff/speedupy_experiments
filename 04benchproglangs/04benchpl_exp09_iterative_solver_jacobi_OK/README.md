# Test Laplace Jacobi Experiment

## Experiment dependencies

The only experiment dependecy is **numpy**. To install it, execute: **pip install numpy**

To run the experiment, make sure you have the appropriate release of SpeeduPy installed. Instructions on which release to use and how to install it can be found [here](https://github.com/dew-uff/memoization/blob/main/README.md#reproducing-the-article-analyses). Ensure that the **speedupy/** folder is located in the same directory as the main experiment script.

## Trials Used in the Article
The five trials used on the memoization techniques article are:

- test_laplace_jacobi_1.py
- test_laplace_jacobi_2.py
- test_laplace_jacobi_3.py
- test_laplace_jacobi_4.py
- test_laplace_jacobi_5.py

To execute a trial, type:

```bash
python speedupy/setup_exp/setup.py test_laplace_jacobi_TRIAL_NUMBER.py
python test_laplace_jacobi_TRIAL_NUMBER.py 10 --exec-mode manual
```
