from interpreter import Interpreter
import sys
import os


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("usage: python computorV2.py [path_to_file]")

    interpreter = Interpreter()
    if len(sys.argv) == 1:
        interpreter.read_eval_print_loop()
    elif len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            print("Wrong file")
            exit(1)
        interpreter.read_eval_file(sys.argv[1])
