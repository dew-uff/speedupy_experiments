# Count Unique Words Experiment

The five trials used on the memoization techniques article use the same script **count_unique_words_speedupy.py** with the following inputs:

- **pg100.txt** (Available at https://www.gutenberg.org/cache/epub/100/pg100.txt)
- **pg9600.txt** (Available at https://www.gutenberg.org/cache/epub/9600/pg9600.txt)
- **pg29090.txt** (Available at https://www.gutenberg.org/cache/epub/29090/pg29090.txt)
- **pg31100.txt** (Available at https://www.gutenberg.org/cache/epub/31100/pg31100.txt)
- **pg52106.txt** (Available at https://www.gutenberg.org/cache/epub/52106/pg52106.txt)

To execute a trial, type:

```bash
python speedupy/setup_exp/setup.py count_unique_words_speedupy.py
python count_unique_words_speedupy.py pg52106.txt --exec-mode manual
```
