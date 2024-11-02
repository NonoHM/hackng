# main.py

from modules.argument_parser import parse_arguments
from modules.file_utils import checker

def main():
    args = parse_arguments()
    checker(args)

if __name__ == '__main__':
    main()
