import sys
sys.path.append('/home/joaopedrolopez/Downloads/AvaliacaoExperimental/Experimentos/speedupy_experiments/04benchproglangs/04benchpl_exp03_count_unique_words_OK')
from speedupy.speedupy import maybe_deterministic
from collections import defaultdict
import sys
import time
from speedupy.speedupy import deterministic, initialize_speedupy
punctuation_characters = "~`!@#$%^&*()_-+=[{]}\\|;:',<.>/?1234567890"

@maybe_deterministic
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
    chunk_size = 300
    words = data.split()
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        partial = new_process_word_chunk_dictionary(chunk)
        for (k, v) in partial.items():
            dictionary[k] += v
    del dictionary['']
    return len(dictionary)

@deterministic
def new_process_word_chunk_dictionary(words):
    partial_dict = defaultdict(int)
    for word in words:
        cleaned = strip_word(word)
        partial_dict[cleaned] += 1
    return partial_dict

@maybe_deterministic
def count_words_set(file_name):
    with open(file_name, 'r') as file_id:
        data = file_id.read()
        return process_count_words_set(data)

@deterministic
def process_count_words_set(data):
    words = data.split()
    uniques = set()
    chunk_size = 300
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        chunk_set = new_process_word_chunk_set(chunk)
        uniques |= chunk_set
    uniques.remove('')
    return len(uniques)

@deterministic
def new_process_word_chunk_set(words):
    return set((strip_word(w) for w in words))
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
    t2 = time.perf_counter()
    print(t1 - t0)
    print(n)
    print('')
if __name__ == '__main__':
    main()