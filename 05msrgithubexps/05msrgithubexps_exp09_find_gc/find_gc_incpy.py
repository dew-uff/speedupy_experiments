import time
import sys


def find_gc(seq):
    """ Calculate GC content """

    if not seq:
        return 0

    gc = len([base for base in seq.upper() if base in 'CG'])
    return (gc * 100) / len(seq)
    
    
   
 

def main(seq):
    print(find_gc(seq))
  

if __name__ == "__main__":
    texto = ''
    with open(sys.argv[1]) as f:
        texto = "".join(f.readlines())
    start = time.time()
    main(texto)
    print(time.time()-start)
