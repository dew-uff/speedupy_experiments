#!/usr/bin/env python

import numpy as np
import scipy.linalg
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "speedupy"))

import time
from speedupy.speedupy import initialize_speedupy, deterministic


@deterministic
def sqrt_matrix(A):
    """
        Take the square root of matrix A
    """
    B = scipy.linalg.sqrtm(A)
    return B

@initialize_speedupy
def main():
    n = int(sys.argv[1])
    A = np.ones((n, n))
    for i in range(n):
        A[i, i] = 6

    dti = time.perf_counter()
    sqrt_matrix(A)
    print(time.perf_counter() - dti)

if __name__ == '__main__':
    main()
