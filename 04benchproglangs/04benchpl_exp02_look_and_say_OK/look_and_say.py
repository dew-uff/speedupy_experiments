#!/usr/bin/env python

import sys
import time

from pathlib import Path
sys.path.append(str(Path(__file__).parent / "speedupy"))

from speedupy.speedupy import deterministic, initialize_speedupy

@deterministic
def look_and_say_sequence(starting_sequence, n):
    i = 0
    while i < n:
        if i == 0:
            current_sequence = starting_sequence
        else:
            count = 1
            temp_sequence = ""
            for j in range(1, len(current_sequence)):
                if current_sequence[j] == current_sequence[j-1]:
                    count += 1
                else:
                    temp_sequence = temp_sequence + str(count) \
                                    + current_sequence[j-1]
                    count = 1
            temp_sequence = temp_sequence + str(count)\
                + current_sequence[len(current_sequence) - 1]

            current_sequence = temp_sequence
        i += 1
    return current_sequence


if len(sys.argv) < 2:
    print('Usage:')
    print('     python ' + sys.argv[0] + ' N')
    print('Please specify a number.')
    sys.exit()

@initialize_speedupy
def main():
    N = int(sys.argv[1])
    t0 = time.perf_counter()
    seq = look_and_say_sequence("1223334444", N)
    print(time.perf_counter() - t0)
    


if __name__ == '__main__':
    main()
