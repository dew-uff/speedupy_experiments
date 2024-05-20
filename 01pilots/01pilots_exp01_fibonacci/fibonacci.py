import time
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent / "speedupy"))

from speedupy.speedupy import initialize_speedupy, deterministic


@deterministic
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


@initialize_speedupy
def main(n):
    print(fib(n))


if __name__ == "__main__":
    n = int(sys.argv[1])
    start = time.perf_counter()
    main(n)
    print(time.perf_counter()-start)
