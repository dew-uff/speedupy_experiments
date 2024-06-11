#!/usr/bin/env python

from collections import defaultdict
import sys
import time

punctuation_characters = "~`!@#$%^&*()_-+=[{]}\|;:',<.>/?1234567890"

def strip_word(word):
    return "".join([x for x in word if x not in
                    punctuation_characters]).strip('\"').lower()

def count_words_dictionary(file_name):
    data = open(file_name).read()
    return process_count_words_dictionary(data)

def process_count_words_dictionary(data):
    dictionary = defaultdict(int)
    for word in data.split():
        dictionary[strip_word(word)] += 1
    del dictionary['']
    return len(dictionary)

def count_words_set(file_name):
    with open(file_name, "r") as file_id:
        data = file_id.read()
        return process_count_words_set(data)

def process_count_words_set(data):
    lines = data.splitlines()
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

def main():
    file_name = sys.argv[1]
    t0 = time.perf_counter()
    n = count_words_dictionary(file_name)
    print(n)
    t1 = time.perf_counter()
    n = count_words_set(file_name)
    print(n)
    t2 = time.perf_counter()
    print(t1-t0)
    print(t2-t1)
    print('')

if __name__ == "__main__":
    main()