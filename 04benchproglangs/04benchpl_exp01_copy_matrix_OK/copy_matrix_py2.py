#!/usr/bin/env python

import numpy as np
import sys
import time


def serial_copy(A,dimension):
    B = np.random.rand(dimension, dimension, 3)
    N = A.shape[0]
    for i in range(N):
        for j in range(N):
            B[i, j, 0] = A[i, j, 1]
            B[i, j, 2] = A[i, j, 0]
            B[i, j, 1] = A[i, j, 2]
    return B

def vector_copy(A,dimension):
    B = np.random.rand(dimension, dimension, 3)
    B[:, :, 0] = A[:, :, 1]
    B[:, :, 2] = A[:, :, 0]
    B[:, :, 1] = A[:, :, 2]
    return B

if len(sys.argv) < 1:
    print 'Usage:'
    print '     python ' + sys.argv[0] + ' dimension'
    print 'Please specify matrix dimensions' 
    sys.exit()

def main():
    dimension = int(sys.argv[1])
    A = np.random.rand(dimension, dimension, 3)
    t0 = time.time()
    serial_copy(A,dimension)
    t1 = time.time()
    vector_copy(A,dimension)
    t2 = time.time()
    print t1-t0 
    print t2-t1 


if __name__ == '__main__':
    main()
