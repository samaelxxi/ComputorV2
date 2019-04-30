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
