from typing import List, Optional, Tuple
from consts import OPERATOR_PRECEDENCE, OPERATOR_MAP
from math_types import AbstractMathType, Operator, Function, Variable
from exceptions.parsing_exceptions import UnexpectedToken
from exceptions.evaluation_exceptions import FunctionNotExists, ExpressionIsNotValid, NoExpectedOperand, VariableNotDefined


class Expression:
    def __init__(self, body):
        self.body = body

    def __len__(self):
        return len(self.body)

    def __str__(self):
        return " ".join(str(obj) for obj in self.body)

    __repr__ = __str__

    def __eq__(self, other):
        print(other)
        if self.body is None and other.body is None:
            return True
        if self.body is None or other.body is None:
            return False
        if len(self.body) != len(other.body):
            return False
        return all(self_el == other_el for self_el, other_el in zip(self.body, other.body))

    def evaluate(self, variables, functions):
        original_body = self.body.copy()
        result = self._evaluate(variables, functions)
        self.body = original_body
        return result

    def _evaluate(self, variables, functions):
        """
        Takes expression and tries to evaluate it

        :param expr: list with operators and operands
        :return: result of expression evaluation, one of math primitive types
        """
        # if (len(self.body) == 1 and isinstance(self.body[0], Function) and  # stupid shit for correction stupid test
        #         self.body[0].name in functions and isinstance(self.body[0].input.body[0], Variable)
        #         and not any(var == self.body[0].input for var in variables.values())
        #         and self.body[0].input == functions[self.body[0].name].input):
        #     return functions[self.body[0].name]


        self._replace_variables(variables)
        self._replace_functions(variables, functions)
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

    def _replace_functions(self, variables, functions) -> None:
        for i, obj in enumerate(self.body):
            if isinstance(obj, Function):
                func_name = obj.name
                if func_name not in functions:
                    raise FunctionNotExists(func_name)

                defined_func = functions[func_name]
                func_var_name = defined_func.input.name
                func_input_expr = obj.input
                func_var_val = func_input_expr.evaluate(variables, functions)
                func_body = defined_func.body
                res = func_body.evaluate({func_var_name: Variable(func_var_name, func_var_val)},
                                         functions)

                self.body[i] = res

    def _replace_variables(self, variables, exceptions: Optional[List[Variable]]=None) -> None:
        """
        Takes expression and replaces all variables by it's values or throws error if it's not defined

        :param expr: list with operators and operands
        """
        for i, obj in enumerate(self.body):
            if isinstance(obj, Variable):
                if exceptions:
                    skip = False
                    for var in exceptions:
                        if var == obj:
                            skip = True
                            break
                    if skip: continue

                var_name = obj.name
                if var_name not in variables:
                    raise VariableNotDefined(var_name)
                self.body[i] = variables[var_name].val

    @staticmethod
    def _get_deepest_brackets(expr: List[AbstractMathType]) -> Tuple[Optional[int], Optional[int]]:
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

    def _evaluate_expression_without_brackets(self, expr: List[AbstractMathType]) -> AbstractMathType:
        """
        Takes simple expression without any bracket and evaluates it

        :param expr: list with operators and operands
        :return: result of expression evaluation, one of math primitive types
        """
        expr_copy = expr[:]
        while True:
            op_idx = self._find_operator_with_highest_prec(expr)
            if op_idx is None:
                if len(expr) != 1:
                    raise ExpressionIsNotValid(expr_copy)
                return expr[0]
            if op_idx == 0 or op_idx == len(expr)-1:
                raise NoExpectedOperand(expr[op_idx].op)
            res = OPERATOR_MAP[expr[op_idx].op](expr[op_idx-1], expr[op_idx+1])
            expr = expr[:op_idx-1] + [res] + expr[op_idx+2:]

    @staticmethod
    def _find_operator_with_highest_prec(expr: List[AbstractMathType]) -> Optional[int]:
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
