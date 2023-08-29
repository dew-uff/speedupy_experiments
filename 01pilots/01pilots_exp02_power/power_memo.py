import time
import sys

from memoizer.DecoratorFactoryInstance import factory

@factory.decorator
def pow(n, m):
    if m == 0:
        return 1
    return n*pow(n, m-1)


def main(n, m):
    print pow(n, m)


if __name__ == "__main__":
    n, m = int(sys.argv[1]), int(sys.argv[2])
    start = time.time()
    main(n, m)
    print time.time()-start
