import time
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'speedupy'))
from speedupy.speedupy import initialize_speedupy, deterministic

@deterministic
def heap_permutation(data, n):
    if n == 1:
        return
    for i in range(n):
        heap_permutation(data, n - 1)
        if n % 2 == 0:
            (data[i], data[n - 1]) = (data[n - 1], data[i])
        else:
            (data[0], data[n - 1]) = (data[n - 1], data[0])
    return data

@initialize_speedupy
def main(n):
    data2 = list(range(n))
    start_time = time.perf_counter()
    heap_permutation(data2, len(data2))
    end_time = time.perf_counter()
    print(end_time - start_time)
if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)