from exceptions import MathException, ParsingError, EvalException, TokenizationError
from exceptions.parsing_exceptions import UnexpectedToken
from exceptions.evaluation_exceptions import (TooManyAssignments, WrongAssingmentLeftPart)
from typing import Tuple, List
from parsing.tokenizer import Tokenizer
from parsing.parser import Parser
from math_types import Operator, Function, Variable, Expression, Equation


class Interpreter:
    """
    Math expressions interpreter
    Supported types:
        Numbers(int or floats)
        Complex Numbers(using i)
        Matrices
        Variables
        Functions
    Variables and functions could be defined usign assignment operator
    Also, simple equations of degree 0-2 is supported. Every term should be in correct form:
        [coefficient][*][variable][^degree]
    """
    def __init__(self):
        self._variables = {}
        self._functions = {}
        self._parser = Parser()
        self._tokenizer = Tokenizer()

    def read_eval_print_loop(self) -> None:
        """
        Infinite REP loop which stops after key interrupt
        """
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
        """
        :param string: input to interpreter
        :return: output as string
        """
        tokens = self._tokenizer.tokenize(string)
        objs = self._parser.parse(tokens)

        op_type, left, right = self._recognize_operation_type(objs)

        if op_type == "assignment":
            eval_res = self._make_assignment(left, right)
        elif op_type == "evaluation":
            eval_res = Expression(left).evaluate(self._variables, self._functions)
        elif op_type == "equation":
            equation = Equation(left, right[:-1], self._variables, self._functions)
            eval_res = equation.solve()
        else:
            raise Exception("Shouldn't be here man")

        return str(eval_res)

    def _make_assignment(self, left: List, right: List) -> str:
        if len(left) != 1:
            raise WrongAssingmentLeftPart(left[0])
        left = left[0]

        if isinstance(left, Variable):
            right_part_evaluated = Expression(right).evaluate(self._variables, self._functions)
            left.val = right_part_evaluated
            self._variables[left.name] = left
            output = right_part_evaluated

        elif isinstance(left, Function):
            if len(left.input) != 1 or not isinstance(left.input.body[0], Variable):
                raise WrongAssingmentLeftPart(left.input)
            left_input_variable = left.input.body[0]
            func_body = Expression(right)
            func_body.evaluate_variables(self._variables, exceptions=[left_input_variable])
            left.body = func_body
            left.input = left_input_variable
            self._functions[left.name] = left
            output = str(left)

        else:
            raise WrongAssingmentLeftPart(left)

        return output

    @staticmethod
    def _recognize_operation_type(expr: List) \
            -> Tuple[str, List, List]:
        """
        Goes through expression, tries to find strange errors and recognize,
        what type of expression this is: "evaluation", "assignment" or "equation"

        :param expr: list with operators and operands
        :return: (one of "evaluation", "assignment" or "equation",
                  list of expression parts, splitted by "=" operator)
        """
        assignment_indices = []
        question_mark = False
        # find assignment operators and question marks. Raise exception if question mark not at the end
        for i, obj in enumerate(expr):
            if isinstance(obj, Operator) and obj.op == "=":
                assignment_indices.append(i)
            elif isinstance(obj, Operator) and obj.op == "?":
                if i != len(expr)-1:
                    raise UnexpectedToken(obj.op)
                question_mark = True

        if len(assignment_indices) > 1:
            raise TooManyAssignments()
        # split input in two parts by assignment operator
        if not assignment_indices:
            left, right = expr, None
        else:
            left = expr[:assignment_indices[0]]
            right = expr[assignment_indices[0]+1:]

        if (question_mark and len(right) == 1) or right is None:
            op_type = "evaluation"   # 'expression = ?' or no assignment operator line
        elif question_mark and len(right) > 1:
            op_type = "equation"
        elif assignment_indices and not question_mark:
            op_type = "assignment"
        else:
            raise Exception("Shouldn't be here man")

        return op_type, left, right
