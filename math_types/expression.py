from typing import List, Optional, Tuple, Dict
from consts import OPERATOR_PRECEDENCE, OPERATOR_MAP
from math_types import Variable, MathPrimitive, Matrix, Number, ComplexNumber, AFunction
from math_types.operator import Operator
from exceptions.parsing_exceptions import UnexpectedToken
from exceptions.evaluation_exceptions import FunctionNotExists, ExpressionIsNotValid, \
    NoExpectedOperand, VariableNotDefined, WrongMatrixElementType


class Expression:
    def __init__(self, body):
        self.body = body
        self._preprocess_expression()

    def __len__(self):
        return len(self.body)

    def __str__(self):
        return " ".join(str(obj) for obj in self.body)

    __repr__ = __str__

    def __eq__(self, other):
        if self.body is None and other.body is None:
            return True
        if self.body is None or other.body is None:
            return False
        if len(self.body) != len(other.body):
            return False
        return all(self_el == other_el for self_el, other_el in zip(self.body, other.body))

    def evaluate(self, variables: Dict[str, Variable],
                       functions: Dict[str, AFunction]) -> MathPrimitive:
        """
        Tries to evaluate self using simple algorithm:
        while expression not simple(one term):
            find deepest nested brackets
            evaluate expression inside brackets and replace it with result

        :param variables: dictionary of defined variables
        :param functions: dictionary of defined functions
        :return: result of evaluation
        """
        original_body = self.body.copy()
        result = self._evaluate(variables, functions)
        self.body = original_body
        return result

    def _preprocess_expression(self):
        objs = self._preprocess_hidden_multiplication(self.body)
        objs = self._preprocess_unary_minus(objs)
        self.body = objs

    def _evaluate(self, variables: Dict[str, Variable],
                        functions: Dict[str, AFunction]) -> MathPrimitive:
        """
        Helper function for self.evaluate
        """
        # if (len(self.body) == 1 and isinstance(self.body[0], Function) and  # stupid shit for correction stupid test
        #         self.body[0].name in functions and isinstance(self.body[0].input.body[0], Variable)
        #         and not any(var == self.body[0].input for var in variables.values())
        #         and self.body[0].input == functions[self.body[0].name].input):
        #     return functions[self.body[0].name]
        self._evaluate_matrices(variables, functions)
        self.evaluate_variables(variables)
        self._evaluate_functions(variables, functions)

        res_expr = self.body[:]
        while True:
            idx1, idx2 = self._get_deepest_brackets(res_expr)
            if idx1 is None:
                res = self._evaluate_expression_without_brackets(res_expr)
                break
            no_brackets_expr = res_expr[idx1+1:idx2]
            res = self._evaluate_expression_without_brackets(no_brackets_expr)
            res_expr = res_expr[:idx1] + [res] + res_expr[idx2+1:]
        return res

    def _evaluate_matrices(self, variables: Dict[str, Variable],
                                 functions: Dict[str, AFunction]) -> None:
        """
        Searches for matrices in self.body and tries to evaluate their elements

        :param variables: dictionary of defined variables
        :param functions: dictionary of defined functions
        """
        for obj in self.body:
            if isinstance(obj, Matrix):
                for row_idx in range(obj.rows):
                    for col_idx in range(obj.cols):
                        matrix_elem = obj.matrix[row_idx][col_idx].evaluate(variables, functions)
                        if not isinstance(matrix_elem, (Number, ComplexNumber)):
                            raise WrongMatrixElementType(matrix_elem)
                        obj.matrix[row_idx][col_idx] = matrix_elem

    def _evaluate_functions(self, variables: Dict[str, Variable],
                            functions: Dict[str, AFunction]) -> None:
        """
        Searches for functions in self.body and tries to evaluate them using definition from given dict

        :param variables: dictionary of defined variables
        :param functions: dictionary of defined functions
        """
        for i, obj in enumerate(self.body):
            if isinstance(obj, AFunction):
                func_name = obj.name
                if func_name not in functions:
                    raise FunctionNotExists(func_name)

                res = functions[func_name].evaluate(obj.input, variables, functions)

                self.body[i] = res

    def evaluate_variables(self, variables: Dict[str, Variable],
                           exceptions: Optional[List[Variable]]=None) -> None:
        """
        Takes expression and replaces all variables by it's values or throws error if variable not defined

        :param variables: dictionary of defined variables
        :param exceptions: list of variables which shouldn't be evaluated
        """
        for i, obj in enumerate(self.body):
            if isinstance(obj, Variable):
                if exceptions and obj in exceptions:
                    continue

                var_name = obj.name
                if var_name not in variables:
                    raise VariableNotDefined(var_name)
                self.body[i] = variables[var_name].val

    @staticmethod
    def _get_deepest_brackets(expr: List) -> Tuple[Optional[int], Optional[int]]:
        """
        Searches for deepest pair of brackets in expression

        :param expr: list with operators and operands
        :return: indeces of opening and closing brackets
        """
        open_idx, close_idx = None, None
        for i, obj in enumerate(expr):
            if isinstance(obj, Operator):
                if obj.op == "(":
                    open_idx = i
                elif obj.op == ")":
                    close_idx = i
                    break
        return open_idx, close_idx

    @staticmethod
    def _evaluate_expression_without_brackets(expr: List) -> MathPrimitive:
        """
        Takes simple expression (as list) without any bracket and evaluates it

        :param expr: list with operators and operands
        :return: result of expression evaluation, one of math primitive types
        """
        expr_copy = expr[:]
        while True:
            op_idx = Expression._find_operator_with_highest_prec(expr)
            if op_idx is None:
                if len(expr) != 1:
                    raise ExpressionIsNotValid(expr_copy)
                return expr[0]
            if op_idx == 0 or op_idx == len(expr)-1:
                raise NoExpectedOperand(expr[op_idx].op)
            res = OPERATOR_MAP[expr[op_idx].op](expr[op_idx-1], expr[op_idx+1])
            expr = expr[:op_idx-1] + [res] + expr[op_idx+2:]

    @staticmethod
    def _find_operator_with_highest_prec(expr: List) -> Optional[int]:
        """
        Searches for operator with highest precedence in expression without brackets

        :param expr: list with operators and operands
        :return: index of highest order operator
        """
        prec_val, op_idx = None, None
        for i, obj in enumerate(expr):
            if isinstance(obj, Operator):
                if obj.op not in OPERATOR_PRECEDENCE:
                    raise UnexpectedToken(obj.op)
                if prec_val is None or OPERATOR_PRECEDENCE[obj.op] > prec_val:
                    prec_val = OPERATOR_PRECEDENCE[obj.op]
                    op_idx = i
        return op_idx

    @staticmethod
    def _preprocess_unary_minus(expr: List) -> List:
        """
        Moves through expression and transform every unary minus to (-1 * val) expression

        :param expr: list with operators and operands
        :return: updated expression
        """
        new_expr = []

        i = 0
        while i < len(expr):
            if (isinstance(expr[i], Operator) and expr[i].op == '-'):   # replace -2 with   (-1 * 2)
                if ((i == 0 or (i != 0 and type(expr[i-1]) is Operator and expr[i-1].op not in ")]"))
                        and i != (len(expr)-1)
                        and type(expr[i+1]) in (Number, ComplexNumber, Matrix, Variable, AFunction)):
                    new_expr.extend([Operator("("), Number(-1), Operator("*"), expr[i+1], Operator(")")])
                    i += 2
                    continue
            new_expr.append(expr[i])
            i += 1
        return new_expr

    @staticmethod
    def _preprocess_hidden_multiplication(expr: List) -> List:
        """
        Moves through expression and transforms every hidden multiplication
        such as 2x or 4i to 2*i or 4*i
        :param expr: list with operators and operands
        :return: updated expression
        """
        new_expr = []
        i = 0
        while i < len(expr):
            if (isinstance(expr[i], Number) and i != len(expr)-1 and
                    isinstance(expr[i+1], (Variable, ComplexNumber))):
                new_expr.extend([expr[i], Operator("*"), expr[i+1]])
                i += 1
            else:
                new_expr.append(expr[i])
            i += 1
        return new_expr
