#!/usr/bin/env python

import numpy as np
import sys

import time

from speedupy.speedupy import initialize_speedupy, deterministic

#--------------------------------
# Function: matrix_multiplication
#--------------------------------

@deterministic
def matrix_multiplication(A, B):
    """
        Evaluate the dot product of matrices A and B using numpy
    """
    C = np.dot(A, B)
    return C

@initialize_speedupy
def main(A,B):
    matrix_multiplication(A, B)

if __name__ == '__main__':
    np.random.seed(0)
    N = int(sys.argv[1])
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)
    dti = time.perf_counter()
    main(A,B)
    print(time.perf_counter() - dti)