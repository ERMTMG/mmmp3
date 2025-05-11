from dir_iter import *
from meta_edit import *
import sys
import argparse
from argparse import ArgumentParser

#def main(exec_name: str, argv: list[str]):
#    iter_directories(argv)
        
def main(argv: list[str], verbose: bool, safety_level: int, autoplay: bool, spanish: bool):
    iter_directories(argv)

if __name__ == '__main__':
    parser: ArgumentParser = ArgumentParser(
        prog='MMMP3',
        description='A program to edit MP3 file metadata swiftly, en-masse or individually'
    )
    parser.add_argument('directories', nargs='+',
                        help='The directories over which the program will operate.')
    parser.add_argument('--verbose', '--verbosity', '-v', action='store_true',
                        help='Will notify of each individual file edited when enabled.')
    parser.add_argument('--safety', '-s', type=int, nargs='?', default=1, const=1,
                        help='Level of sensitivity to editing files. The higher it is, '
                        'the more confirmation will be asked to edit files. '
                        'Default is 1, min is 0 and max is 3.')
    parser.add_argument('--autoplay', '-a', action='store_true',
                        help='Autoplays each song when editing MP3s in a directory.')
    parser.add_argument('--español', '-ñ', action='store_true',
                        help='Muestra la interfaz en español.')
    args: argparse.Namespace = parser.parse_args()
    main(args.directories)
     
