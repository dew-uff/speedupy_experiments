import numpy as np
from scipy.optimize import fsolve
import time
import sys
from speedupy.speedupy import initialize_speedupy, deterministic

@deterministic
def solve(n, F_solution):
    T = 1
    C = 1
    Kd1 = 2
    n2 = 1000
    Kd2 = 1
    return fsolve(func=lambda x: n * C / (1 + Kd1 / x) + n2 * C / (1 + Kd2 / x) - T, x0=F_solution, xtol=1e-06)

@deterministic
def exp_main(F_solution):
    n_solutions = 400000
    x_list = np.linspace(1, 20000.0, n_solutions)
    F_list = np.empty_like(x_list)
    for i in range(n_solutions):
        F_solution = solve(x_list[i], F_solution)
        F_list[i] = F_solution
    return (F_list, F_solution)

@initialize_speedupy
def main():
    F_solution = int(sys.argv[1])
    F_solution = F_solution / 10
    start = time.perf_counter()
    exp_main(F_solution)
    print(time.perf_counter() - start)
if __name__ == '__main__':
    main()