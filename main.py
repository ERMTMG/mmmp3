from dir_iter import *
from meta_edit import *
import sys

def main(exec_name: str, argv: list[str]):
    for arg in argv:
        if os.path.isdir(arg):
            pass
        else:
            print('oops! ', arg, ' is not a directory!\n')
    print('\n')
        

if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
