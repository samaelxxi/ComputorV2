from interpreter import Interpreter
import sys
import os


"""
TODO
Functionality:
Bonuses:
    Special function (sin, cos, tan, abs, sqrt...)
    Special commands (plot, vars)
    Matrix inversion?

stupid fucking test_54 for stupid correction form

Cool things:
Parsing is ugly as shit goddamnit
- SOLID
2. Refactor shit
4. Use generators? (nowhere))
5. decorators?
6. Why I'm using annotations?
8. wtf classmethod? ok it's like static but it takes class so could be used with inheritance and make factories maybe
- Data descriptors(class which has __get__ and __set__), properties, __slots__


DONE:
1. Add equations(tests first)
0. Matrices + Complex Numbers?
- Crazy powers leading to complex numbers...
except  OverflowError, ZeroDivisionError     
matmul operator between other types...
Matrix parser negative values and any expression
7. Assignment of functions to variables...
- Move all constants somewhere
3. Replace lists with expression class? And so implement iterators for them(why)
"""


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
        interpreter.read_eval_print_file(sys.argv[1])
