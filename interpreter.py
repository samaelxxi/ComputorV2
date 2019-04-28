"""Interpreter class which implements REP loop"""
from parsing.tokenizer import Tokenizer
from parsing.parser import Parser
from math_types import Operator, Number, ComplexNumber, Matrix, Function, Variable,  Expression, MATH_TYPES, AbstractMathType
from exceptions import MathException, ParsingError, EvalException, TokenizationError
from exceptions.parsing_exceptions import UnexpectedToken
from exceptions.evaluation_exceptions import (TooManyAssignments, WrongAssingmentLeftPart)
from typing import Tuple, List


class Interpreter:
    def __init__(self):
        self._variables = {}
        self._functions = {}
        self._parser = Parser()
        self._tokenizer = Tokenizer()

    def read_eval_print_loop(self) -> None:
        while True:
            try:
                input_string = input(">")
            except (EOFError, KeyboardInterrupt):
                break
            self.eval_print_string(input_string)

    def read_eval_print_file(self, filename: str) -> None:
        file = open(filename, "r")
        for line in file:
            self.eval_print_string(line)

    def eval_print_string(self, input_string: str) -> None:
        try:
            if input_string:
                output_string = self.eval_string(input_string)
                print(output_string)
        except (ParsingError, EvalException, MathException, TokenizationError) as e:
            print("ERROR: ", str(e))

    def eval_string(self, string: str) -> str:
        tokens = self._tokenizer.tokenize(string)
        objs = self._parser.parse(tokens)

        op_type, left, right = self._recognize_operation_type(objs)
        left = self._preprocess_objects(left)
        right = self._preprocess_objects(right)
        if op_type == "assignment":
            eval_res = self._make_assignment(left, right)
        elif op_type == "evaluation":
            eval_res = Expression(left).evaluate(self._variables, self._functions)
        elif op_type == "equation":
            raise Exception("Not implemented!")
            eval_res = None
            pass
        else:
            raise Exception("Shouldn't be here man")

        return str(eval_res)

    def _preprocess_objects(self, objs):
        if objs is None: return None
        objs = self._preprocess_hidden_multiplication(objs)
        objs = self._preprocess_unary_minus(objs)
        return objs

    def _make_assignment(self, left: List[AbstractMathType], right: List[AbstractMathType]) -> str:
        if len(left) != 1:
            raise WrongAssingmentLeftPart(left[0])
        left = left[0]

        if isinstance(left, Variable):
            right_part_evaluated = Expression(right).evaluate(self._variables, self._functions)
            left.val = right_part_evaluated
            self._variables[left.name] = left
            output = right_part_evaluated

        elif isinstance(left, Function):
            print(left.input, left.input.body)
            if len(left.input) != 1 or not isinstance(left.input.body[0], Variable):
                raise WrongAssingmentLeftPart(left.input)
            left_input = left.input.body[0]
            func_body = Expression(right)
            func_body._replace_variables(self._variables, exceptions=[left_input])
            left.body = func_body
            left.input = left_input
            self._functions[left.name] = left
            output = str(left)

        else:
            raise WrongAssingmentLeftPart(left)

        return output

    @staticmethod
    def _preprocess_unary_minus(expr: List[AbstractMathType]) -> List[AbstractMathType]:  # TODO move to parser?
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
    def _preprocess_hidden_multiplication(expr: List[AbstractMathType]) -> List[AbstractMathType]:
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
    def _recognize_operation_type(expr: List[AbstractMathType]) \
            -> Tuple[str, List[AbstractMathType], List[AbstractMathType]]:
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

        if not assignment_indices:
            left, right = expr, None
        else:
            left  = expr[:assignment_indices[0]]
            right = expr[assignment_indices[0]+1:]

        if (question_mark and len(right) == 1) or right is None: # 'expression = ?' or no assignment operator line
            op_type = "evaluation"
        elif question_mark and len(right) > 1:
            op_type = "equation"
        elif assignment_indices and not question_mark:
            op_type = "assignment"
        else:
            raise Exception("Shouldn't be here man")

        return op_type, left, right
