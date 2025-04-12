from dir_iter import *
from meta_edit import *
import sys

def main(exec_name: str, argv: list[str]):
    iter_directories(argv)
        

if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
