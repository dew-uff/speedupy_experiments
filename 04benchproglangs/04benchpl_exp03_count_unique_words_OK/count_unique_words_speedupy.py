import sys
sys.path.append('/home/joaopedrolopez/Downloads/AvaliacaoExperimental/Experimentos/speedupy_experiments/04benchproglangs/04benchpl_exp03_count_unique_words_OK')
from speedupy.speedupy import maybe_deterministic
from collections import defaultdict
import sys
import time
from speedupy.speedupy import deterministic, initialize_speedupy
punctuation_characters = "~`!@#$%^&*()_-+=[{]}\\|;:',<.>/?1234567890"

@deterministic
def strip_word(word):
    temp1 = ''
    temp1 = temp1.join([x for x in word if x not in punctuation_characters])
    temp1 = temp1.strip('"')
    return temp1.lower()

@maybe_deterministic
def count_words_dictionary(file_name):
    temp2 = open(file_name)
    data = temp2.read()
    return process_count_words_dictionary(data)

@deterministic
def process_count_words_dictionary(data):
    dictionary = defaultdict(int)
    for word in data.split():
        dictionary[strip_word(word)] += 1
    del dictionary['']
    return len(dictionary)

@maybe_deterministic
def count_words_set(file_name):
    with open(file_name, 'r') as file_id:
        data = file_id.read()
        return process_count_words_set(data)

@deterministic
def process_count_words_set(data):
    lines = data.splitlines()
    uniques = set()
    for line in lines:
        uniques |= set((strip_word(m) for m in line.split()))
    uniques.remove('')
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
    print(t1 - t0)
    print(t2 - t1)
    print('')
if __name__ == '__main__':
    main()