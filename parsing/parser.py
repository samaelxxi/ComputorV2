"""Parser class implementation"""

from math_types import Operator, Number, ComplexNumber, Matrix, Function, Variable
from exceptions.parsing_exceptions import (BracketsMismatch, NoClosingBracket,
                                           UnknownToken, BadNumber, MatrixDiffElems,
                                           UnexpectedToken, EmptyMatrix, ExtraBracket)


OPERATOR_TOKENS = ["+", "-", "*", "/", "%", "^", "=", "**", "?", "(", ")", "[", "]", ",", ";"]


class Parser:
    """Parser takes tokens and builds objects from it"""
    def parse(self, tokens):
        """
        Parses all tokens at first into simple math_types at first
            then tries to build complex types from simple ones
        :param tokens: list of tokens as strings
        :return: list of math_types objects
        """
        self._check_brackets(tokens)

        objs = self._parse_individual_tokens(tokens)
        objs = self._parse_functions(objs)
        objs = self._parse_matrices(objs)

        return objs

    @staticmethod
    def _check_brackets(tokens):
        brackets = []
        for token in tokens:
            if token in "([":
                brackets.append(token)
            elif token in ")]":
                if not brackets:
                    raise ExtraBracket(token)
                closing_bracket = brackets.pop()
                if ((token == "(" and closing_bracket != ")") or
                        (token == "[" and closing_bracket != "]")):
                    raise BracketsMismatch(token, closing_bracket)
        if brackets:
            raise NoClosingBracket(brackets[0])
        return True

    def _parse_individual_tokens(self, tokens):
        objs = []

        for token in tokens:
            obj = self._parse_token(token)
            objs.append(obj)

        return objs

    @staticmethod
    def _parse_token(token):
        if token in OPERATOR_TOKENS:
            return Operator(token)
        if token.isdigit():
            return Number(int(token))
        if "." in token:
            if token.count(".") > 1:
                raise BadNumber(token)
            return Number(float(token))
        if token == "i":
            return ComplexNumber(0, 1)
        if token.isalpha():
            return Variable(token)
        raise UnknownToken(token)

    @staticmethod
    def _parse_functions(objs):
        is_func_body = False
        func_start_idx = None
        new_objs = []
        for i, obj in enumerate(objs):
            if is_func_body:
                if isinstance(obj, Operator) and obj.op == ")":
                    is_func_body = False
                    if i - func_start_idx == 3: # one item inside brackets
                        new_objs.append(Function(name=objs[func_start_idx].name,
                                                 input_=objs[i-1]))
                    else:
                        raise Exception("Too many shit in function input")
            elif (isinstance(obj, Variable) and i+1 != len(objs) and
                  isinstance(objs[i+1], Operator) and objs[i+1].op == "("):
                func_start_idx = i
                is_func_body = True
            else:
                new_objs.append(obj)

        return new_objs

    def _parse_matrices(self, objs):
        new_objs = objs[:]
        while True:
            idx1, idx2 = self._locate_matrix(new_objs)
            if idx1 is None:
                break
            else:
                matrix = self._parse_matrix(new_objs[idx1:idx2])
                new_objs = new_objs[:idx1] + [matrix] + new_objs[idx2:]
        return new_objs

    @staticmethod
    def _locate_matrix(objs):
        depth = 0
        in_matrix = False
        idx1, idx2 = None, None

        for i, obj in enumerate(objs):
            if isinstance(obj, Operator):
                if obj.op == "[":
                    if not in_matrix:
                        in_matrix = True
                        idx1 = i
                    depth += 1
                elif obj.op == "]":
                    depth -= 1
                    if depth == 0:
                        idx2 = i+1
                        return idx1, idx2
        return idx1, idx2

    @staticmethod
    def _parse_matrix(objs):
        matrix = Matrix(0, 0, [])
        objs = objs[1:-1]  # remove outer brackets
        exp = "["
        cur_row = []
        for obj in objs:
            if isinstance(obj, Operator):
                if obj.op not in exp:
                    raise UnexpectedToken(obj)
                if obj.op == "[":
                    exp = "object"
                    cur_row = []
                elif obj.op == ",":
                    exp = "object"
                elif obj.op == ";":
                    exp = "["
                elif obj.op == "]":
                    exp = ";"
                    matrix.matrix.append(cur_row)
                    matrix.rows += 1
                    if matrix.cols == 0:
                        matrix.cols = len(cur_row)
                    else:
                        if matrix.cols != len(cur_row):
                            raise MatrixDiffElems
            elif exp == "object" and isinstance(obj, (Number, ComplexNumber, Variable)):
                cur_row.append(obj)
                exp = (",", "]")
            else:
                raise UnexpectedToken(obj)
        if matrix.rows == 0:
            raise EmptyMatrix()
        return matrix
