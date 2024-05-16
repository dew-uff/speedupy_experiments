#!/usr/bin/env python

from collections import defaultdict
import sys
import time
from speedupy.speedupy import deterministic, initialize_speedupy

punctuation_characters = "~`!@#$%^&*()_-+=[{]}\|;:',<.>/?1234567890"

@deterministic
def strip_word(word):
    temp1 = ""
    temp1 = temp1.join([x for x in word if x not in punctuation_characters]) 
    temp1 = temp1.strip('\"')
    return temp1.lower()

@deterministic
def count_words_dictionary(file_name):
    dictionary = defaultdict(int)
    temp2 = open(file_name)
    temp2 = temp2.read()
    for word in temp2.split():
        dictionary[strip_word(word)] += 1
    del dictionary['']
    return len(dictionary)

@deterministic 
def count_words_set(file_name):
    with open(file_name, "r") as file_id:
        temp3 = file_id.read()
        lines = temp3.splitlines()
        uniques = set()
        for line in lines:
            uniques |= set(strip_word(m) for m in line.split())
    uniques.remove('')
    #print(uniques)
    return len(uniques)


if len(sys.argv) < 1:
    print('Usage:')
    print('     python ' + sys.argv[0] + ' file_name')
    print('Please specify the file name')
    sys.exit()

@initialize_speedupy
def main():
    file_name = sys.argv[1]
    t0 = time.perf_counter()
    n = count_words_dictionary(file_name)
    t1 = time.perf_counter()
    n = count_words_set(file_name)
    t2 = time.perf_counter()
    print(t1-t0)
    print(t2-t1)
    print('')

if __name__ == "__main__":
    main()