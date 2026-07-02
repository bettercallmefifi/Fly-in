# main.py
import sys
from parsing import Parser, ParsingError

def valid_arg() -> str:
    if len(sys.argv) != 2:
        print("Invalid arguments")
        sys.exit(1)
    return sys.argv[1]

def main():
    file_name = valid_arg()
    parser = Parser(file_name)
    
    try:
        parser.parsing()
        parser.parse_nb_drones()
    except ParsingError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()