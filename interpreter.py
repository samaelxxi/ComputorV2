"""Interpreter class which implements REP loop"""
from parsing.tokenizer import Tokenizer
from parsing.parser import Parser
from math_types import Operator, Number, ComplexNumber, Matrix, Function, Variable, MATH_TYPES
from exceptions import MathException, ParsingError, EvalException, TokenizationError
from exceptions.parsing_exceptions import UnexpectedToken
from exceptions.evaluation_exceptions import (TooManyAssignments, WrongAssingmentLeftPart,
                                              NoExpectedOperand, ExpressionIsNotValid,
                                              VariableNotDefined, FunctionNotExists)
import operator
from copy import deepcopy


OPERATOR_PRECEDENCE = {"+": 0, "-": 0, "%": 1, "*": 2, "/": 2, "^": 3, "**": 2}
OPERATOR_MAP = {"+": operator.add,
                "-": operator.sub,
                "%": operator.mod,
                "*": operator.mul,
                "/": operator.truediv,
                "^": operator.xor,
                "**": operator.pow}


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.parser = Parser()
        self.tokenizer = Tokenizer()

    def read_eval_print_loop(self):
        while True:
            try:
                input_string = input(">")
                if not input_string: continue
                output_string = self.eval(input_string)
                print(output_string)
            except (ParsingError, EvalException, MathException, TokenizationError) as e:
                print("ERROR: ", str(e))
            except (EOFError, KeyboardInterrupt):
                print()
                break

    def read_eval_file(self, filename):
        file = open(filename, "r")
        for line in file:
            try:
                output_string = self.eval(line)
                print(output_string)
            except (ParsingError, EvalException, MathException, TokenizationError) as e:
                print("ERROR: ", str(e))

    def eval(self, string):
        tokens = self.tokenizer.tokenize(string)
        objs = self.parser.parse(tokens)

        op_type, parts = self._recognize_operation_type(objs)
        parts = [self._preprocess_hidden_multiplication(part) for part in parts]
        parts = [self._preprocess_unary_minus(part) for part in parts]

        if op_type == "assignment":
            eval_res = self._make_assignment(parts)
        elif op_type == "evaluation":
            eval_res = self._evaluate_expression(parts[0])
        elif op_type == "equation":
            raise Exception("Not implemented!")
            eval_res = None
            pass
        else:
            raise Exception("Shouldn't be here man")

        return str(eval_res)

    def _make_assignment(self, expr_parts):
        if len(expr_parts[0]) != 1:
            raise WrongAssingmentLeftPart(expr_parts)
        left_part = expr_parts[0][0]
        right_part = expr_parts[1]

        if isinstance(left_part, Variable):
            right_part_evaluated = self._evaluate_expression(right_part)
            left_part.val = right_part_evaluated
            self.variables[left_part.name] = left_part
            output = right_part_evaluated

        elif isinstance(left_part, Function):
            if not isinstance(left_part.input, Variable):
                raise WrongAssingmentLeftPart(left_part)
            self._replace_variables(right_part, exceptions=[left_part.input])
            left_part.body = right_part
            self.functions[left_part.name] = left_part
            output = str(left_part)

        else:
            raise WrongAssingmentLeftPart(left_part)

        return output

    def _evaluate_expression(self, expr):
        """
        Takes expression and tries to evaluate it

        :param expr: list with operators and operands
        :return: result of expression evaluation, one of math primitive types
        """
        if (len(expr) == 1 and isinstance(expr[0], Function) and  # stupid shit for correction stupid test
                expr[0].name in self.functions and isinstance(expr[0].input, Variable)
                and not any(var == expr[0].input for var in self.variables.values())
                and expr[0].input == self.functions[expr[0].name].input):
            return str(self.functions[expr[0].name])

        self._replace_variables(expr)
        self._replace_functions(expr)
        while True:
            idx1, idx2 = self._get_deepest_brackets(expr)
            if idx1 is None:
                res = self._evaluate_expression_without_brackets(expr)
                break
            no_brackets_expr = expr[idx1+1:idx2]
            res = self._evaluate_expression_without_brackets(no_brackets_expr)
            expr = expr[:idx1] + [res] + expr[idx2+1:]
        return res

    def _replace_functions(self, expr):
        for i, obj in enumerate(expr):
            if isinstance(obj, Function):
                func_name = obj.name
                if func_name not in self.functions:
                    raise FunctionNotExists(func_name)

                defined_func = self.functions[func_name]
                func_var_name = defined_func.input.name
                func_var_val = self._evaluate_expression([obj.input])
                func_body = defined_func.body[:]

                temp_interpreter = Interpreter()
                temp_interpreter.variables[func_var_name] = Variable(func_var_name, func_var_val)
                res = temp_interpreter._evaluate_expression(func_body)

                expr[i] = res


    def _replace_variables(self, expr, exceptions=None):
        """
        Takes expression and replaces all variables by it's values or throws error if it's not defined

        :param expr: list with operators and operands
        """
        for i, obj in enumerate(expr):
            if isinstance(obj, Variable):
                if exceptions:
                    skip = False
                    for var in exceptions:
                        if var == obj:
                            skip = True
                            break
                    if skip: continue

                var_name = obj.name
                if var_name not in self.variables:
                    raise VariableNotDefined(var_name)
                expr[i] = self.variables[var_name].val

    @staticmethod
    def _get_deepest_brackets(expr):
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

    def _evaluate_expression_without_brackets(self, expr):
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
    def _find_operator_with_highest_prec(expr):
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
    def _preprocess_unary_minus(expr):  # TODO move to parser?
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
                        and type(expr[i+1]) in MATH_TYPES):
                    new_expr.extend([Operator("("), Number(-1), Operator("*"), expr[i+1], Operator(")")])
                    i += 2
                    continue
            new_expr.append(expr[i])
            i += 1
        return new_expr

    @staticmethod
    def _preprocess_hidden_multiplication(expr):
        """
        Moves through expression and transforms every hidden multiplication
        such as 2x or 4i to 2*i or 4*i
        :param expr: list with operators and operands
        :return: updated expression
        """
        new_expr = []
        i = 0
        while i < len(expr):
            if (isinstance(expr[i], Number) and i != len(expr)-1 and isinstance(expr[i+1], (Variable, ComplexNumber))):
                new_expr.extend([expr[i], Operator("*"), expr[i+1]])
                i += 1
            else:
                new_expr.append(expr[i])
            i += 1
        return new_expr

    @staticmethod
    def _recognize_operation_type(expr):
        """
        Goes through expression, tries to find strange errors and recognize,
        what type of expression this is: "evaluation", "assignment" or "equation"

        :param expr: list with operators and operands
        :return: (one of "evaluation", "assignment" or "equation",
                  list of expression parts, splitted by "=" operator)
        """
        assignment_indices = []
        question_mark = False

        for i, obj in enumerate(expr):
            if isinstance(obj, Operator) and obj.op == "=":
                assignment_indices.append(i)
            elif isinstance(obj, Operator) and obj.op == "?":
                if i != len(expr)-1:
                    raise UnexpectedToken(obj.op)
                question_mark = True

        if len(assignment_indices) > 1:
            raise TooManyAssignments()

        parts = ([expr[:assignment_indices[0]], expr[assignment_indices[0]+1:]]
                 if assignment_indices else [expr])

        if (question_mark and len(parts[1]) == 1) or not assignment_indices: # 'expression = ?' or no assignment operator line
            op_type = "evaluation"
        elif question_mark and len(parts) > 1:
            op_type = "equation"
        elif assignment_indices and not question_mark:
            op_type = "assignment"
        else:
            raise Exception("Shouldn't be here man")

        return op_type, parts
