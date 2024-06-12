from speedupy.speedupy import initialize_speedupy, deterministic
import time
import sys
import numpy as np

@deterministic
def median(vals):
    count = len(vals)
    if count == 1:
        return float(vals[0])
    vals = sorted(vals)
    idx1 = int(count / 2)
    idx2 = idx1 + 1
    if float(idx1) != count / 2.0:
        idx1 = idx2
    return int(vals[idx1] + vals[idx2]) / 2.0

@initialize_speedupy
def main(vals):
    print(median(vals))
if __name__ == '__main__':
    import random
    random.seed(0)
    unsort_list = [random.randint(1, 1000000000000.0) for i in range(int(float(sys.argv[1])))]
    start = time.perf_counter()
    main(unsort_list)
    print(time.perf_counter() - start)