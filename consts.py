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
    "sin": lambda x: Number(round(math.sin(x))),
    "cos": lambda x: Number(round(math.cos(x))),
    "tan": lambda x: Number(round(math.tan(x))),
    "exp": lambda x: Number(round(math.exp(x))),
    "abs": lambda x: Number(round(abs(x))),
    "sqrt": lambda x: Number(round(math.sqrt(x))),
    "log": lambda x: Number(round(math.log(x)))
}
