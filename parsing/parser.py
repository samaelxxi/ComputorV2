"""Parser class implementation"""

from math_types import Operator, Number, ComplexNumber, Matrix, Function, Variable, Expression
from exceptions.parsing_exceptions import (BracketsMismatch, NoClosingBracket,
                                           UnknownToken, BadNumber, MatrixDiffElems,
                                           UnexpectedToken, EmptyMatrix, ExtraBracket)
from typing import List, Tuple, Optional
from consts import OPERATOR_TOKENS


class Parser:
    """Parser takes tokens and builds objects from it"""
    def parse(self, tokens: List[str]) -> List:
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
    def _check_brackets(tokens: List[str]) -> True:
        """
        Takes list of tokens and checks that all brackets are in right order.
        Raises ParsingException if brackets are bad.

        :param tokens: list of tokens
        :return: True
        """
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

    def _parse_individual_tokens(self, tokens: List[str]) -> List:
        """
        Parses simple, not composed tokens

        :param tokens: list of tokens as strings
        :return: list of Operators, Numbers, ComplexNumbers or Variables
        """
        objs = []

        for token in tokens:
            obj = self._parse_token(token)
            objs.append(obj)

        return objs

    @staticmethod
    def _parse_token(token: str):
        """
        Parses simple tokens to simple math objects. Raises exception if token is bad

        :param token: string
        :return: Operator, Number, Complex Number or Variable
        """
        if token in OPERATOR_TOKENS:
            return Operator(token)
        if token.isdigit():
            return Number(int(token))
        if "." in token:
            if token.count(".") > 1 or token[-1] == '.':
                raise BadNumber(token)
            return Number(float(token))
        if token == "i":
            return ComplexNumber(0, 1)
        if token.isalpha():
            return Variable(token)
        raise UnknownToken(token)

    def _parse_functions(self, objs: List) -> List:
        """
        Scans through list of simple math objects and tries to detect and transform
        functions. Function is detected if there's variable with brackets after it.

        :param objs: list of math objects
        :return: updated with functions list of math objects
        """
        is_func_body = False
        func_start_idx = None
        new_objs = []
        for i, obj in enumerate(objs):
            if is_func_body:
                if isinstance(obj, Operator) and obj.op == "(":
                    brackets_inside_func += 1
                elif isinstance(obj, Operator) and obj.op == ")":
                    if brackets_inside_func:
                        brackets_inside_func -= 1
                    else:
                        is_func_body = False
                        func_input = objs[func_start_idx+2:i]
                        func_input = self._parse_functions(func_input)
                        func_input = self._parse_matrices(func_input)
                        func_input = Expression(func_input)
                        new_objs.append(Function(name=objs[func_start_idx].name,
                                                 input_=func_input))

            elif (isinstance(obj, Variable) and i+1 != len(objs) and
                  isinstance(objs[i+1], Operator) and objs[i+1].op == "("):
                func_start_idx = i
                is_func_body = True
                brackets_inside_func = -1
            else:
                new_objs.append(obj)

        return new_objs

    def _parse_matrices(self, objs: List) -> List:
        """
        Scans through list of simple math objects and tries to detect and transform
        matrices. Matrix is detected by square brackets.

        :param objs: list of math objects
        :return: updated with matrices list of math objects
        """
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
    def _locate_matrix(objs: List) -> Tuple[Optional[int], Optional[int]]:
        """
        Locates indices for leftmost and rightmost matrix brackets

        :param objs: list of math objects
        :return: indices for left and right bracket, or None if there's no matrices
        """
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
    def _parse_matrix(objs: List) -> Matrix:
        """
        Takes list of objects that are located inside matrix and parses them
        to matrix object using simple state machine.

        :param objs: list of math objects
        :return: Matrix
        """
        matrix = Matrix(0, 0, [])
        objs = objs[1:-1]  # remove outer brackets
        exp = "["
        cur_row = []
        cur_elem = []
        for obj in objs:
            if isinstance(obj, Operator) and obj.op in ["+", "-", "%", "*", "/", "^", "**", "(", ")"] and "object" in exp:
                cur_elem.append(obj)
                exp = (",", "]", "object")
            elif isinstance(obj, Operator):
                if obj.op not in exp:
                    raise UnexpectedToken(obj)
                if obj.op == "[":
                    exp = "object"
                    cur_row = []
                elif obj.op == ",":
                    exp = "object"
                    cur_row.append(Expression(cur_elem))
                    cur_elem = []
                elif obj.op == ";":
                    exp = "["
                elif obj.op == "]":
                    exp = ";"
                    cur_row.append(Expression(cur_elem))
                    cur_elem = []
                    matrix.matrix.append(cur_row)
                    matrix.rows += 1
                    if matrix.cols == 0:
                        matrix.cols = len(cur_row)
                    else:
                        if matrix.cols != len(cur_row):
                            raise MatrixDiffElems
            elif "object" in exp and isinstance(obj, (Number, ComplexNumber, Variable, Function)):
                cur_elem.append(obj)
                exp = (",", "]", "object")
            else:
                raise UnexpectedToken(obj)
        if matrix.rows == 0:
            raise EmptyMatrix()
        return matrix
