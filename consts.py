import operator

ONE_CHAR_TOKENS = ["+", "-", "*", "/", "%", "^", "(", ")", "=", "?", "[", "]", ",", ";"]
OPERATOR_TOKENS = ["+", "-", "*", "/", "%", "^", "=", "**", "?", "(", ")", "[", "]", ",", ";"]
OPERATOR_PRECEDENCE = {"+": 0, "-": 0, "%": 1, "*": 2, "/": 2, "^": 3, "**": 2}
OPERATOR_MAP = {"+": operator.add,
                "-": operator.sub,
                "%": operator.mod,
                "*": operator.mul,
                "/": operator.truediv,
                "^": operator.xor,
                "**": operator.pow}

from math_types import Number
import math


DEFINED_VARS = {
    "pi": Number(math.pi),
    "e": Number(math.e)
}

DEFINED_FUNCS = {
    "sin": lambda x: Number(round(math.sin(x), 3)),
    "cos": lambda x: Number(round(math.cos(x), 3)),
    "tan": lambda x: Number(round(math.tan(x), 3)),
    "exp": lambda x: Number(round(math.exp(x), 3)),
    "abs": lambda x: Number(round(abs(x), 3)),
    "sqrt": lambda x: Number(round(math.sqrt(x), 3)),
    "log": lambda x: Number(round(math.log(x), 3))
}

from math_types.function import SpecialCommand
from math_types.commands import *

SPECIAL_COMMANDS = {
    "vars": SpecialCommand("vars", vars_command),
    "funcs": SpecialCommand("funcs", funcs_command),
    "plot": SpecialCommand("plot", plot_command),
    "linreg": SpecialCommand("plot", linreg_command)
}
