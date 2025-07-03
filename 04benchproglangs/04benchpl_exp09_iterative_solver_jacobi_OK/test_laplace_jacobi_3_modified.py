import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'speedupy'))
import numpy as np
import time
from speedupy.speedupy import initialize_speedupy, deterministic
import copy

@deterministic
def loop_time_step(u):
    """
        Take a time step in the desired numerical solution 
        u found using loops
    """
    aux = copy.deepcopy(u)
    (n, m) = aux.shape
    error = 0.0
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            temp = aux[i, j]
            aux[i, j] = ((aux[i - 1, j] + aux[i + 1, j] + aux[i, j - 1] + aux[i, j + 1]) * 4.0 + aux[i - 1, j - 1] + aux[i - 1, j + 1] + aux[i + 1, j - 1] + aux[i + 1, j + 1]) / 20.0
            difference = aux[i, j] - temp
            error += difference * difference
    return (aux, np.sqrt(error))

@deterministic
def loop_solver(n, e):
    """
        Find the desired numerical solution using loops
    """
    j = complex(0, 1)
    pi_c = np.pi
    u = np.zeros((n, n), dtype=float)
    x = np.r_[0.0:pi_c:n * j]
    u[0, :] = np.sin(x)
    u[n - 1, :] = np.sin(x) * np.exp(-pi_c)
    iteration = 0
    error = 2
    while iteration < 1000000 and error > e:
        (u, error) = loop_time_step(u)
        iteration += 1
    return (u, error, iteration)

@deterministic
def vector_time_step(u):
    """
        Take a time step in the desired numerical solution v 
        found using vectorization
    """
    aux = copy.deepcopy(u)
    u_old = aux.copy()
    aux[1:-1, 1:-1] = ((aux[0:-2, 1:-1] + aux[2:, 1:-1] + aux[1:-1, 0:-2] + aux[1:-1, 2:]) * 4.0 + aux[0:-2, 0:-2] + aux[0:-2, 2:] + aux[2:, 0:-2] + aux[2:, 2:]) / 20.0
    return (aux, np.linalg.norm(aux - u_old))

@deterministic
def vectorized_solver(n, e):
    """
        Find the desired numerical solution using vectorization
    """
    j = complex(0, 1)
    pi_c = np.pi
    u = np.zeros((n, n), dtype=float)
    x = np.r_[0.0:pi_c:n * j]
    u[0, :] = np.sin(x)
    u[n - 1, :] = np.sin(x) * np.exp(-pi_c)
    iteration = 0
    error = 2
    while iteration < 1000000 and error > e:
        (u, error) = vector_time_step(u)
        iteration += 1
    return (u, error, iteration)

@initialize_speedupy
def main():
    num_points = int(sys.argv[1])
    dti = time.perf_counter()
    (u, error, iteration) = loop_solver(num_points, 1e-08)
    print(time.perf_counter() - dti)
    dti = time.perf_counter()
    (u, error, iteration) = vectorized_solver(num_points, 1e-08)
    print(time.perf_counter() - dti)
if __name__ == '__main__':
    main()