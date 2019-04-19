"""Interpreter class which implements REP loop"""
from parsing.tokenizer import Tokenizer
from parsing.parser import Parser
from math_types import Operator, Number, ComplexNumber, Matrix, Function, Variable
from exceptions import MathException, ParsingError, EvalException, TokenizationError
from exceptions.parsing_exceptions import UnexpectedToken
from exceptions.evaluation_exceptions import TooManyAssignments


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.parser = Parser()
        self.tokenizer = Tokenizer()

    def eval(self, string):
        tokens = self.tokenizer.tokenize(string)
        objs = self.parser.parse(tokens)

        op_type, parts = self._recognize_operation_type(objs)
        objs = self._preprocess_unary_minus(parts)
        # detect type of operation
        # if assignment operator in ops and question mark is not, split by it and check left part if it's var or eq


    @staticmethod
    def _preprocess_unary_minus(parts):
        for objs in parts:
            for i, obj in enumerate(objs):
                if isinstance(obj, Operator):pass
        pass

    @staticmethod
    def _recognize_operation_type(objs):
        assignment_indices = []
        question_mark = False
        for i, obj in enumerate(objs):
            if isinstance(obj, Operator) and obj.op == "=":
                assignment_indices.append(i)
            elif isinstance(obj, Operator) and obj.op == "?":
                if i != len(objs):
                    raise UnexpectedToken(obj.op)
                question_mark = True
        if len(assignment_indices) > 1:
            raise TooManyAssignments()

        parts = [objs[:assignment_indices[0]], objs[assignment_indices[0]:]] if assignment_indices else [objs]
        if (question_mark and len(parts) == 1) or not assignment_indices: # 'expression = ?' or no assignment operator line
            op_type = "evaluation"
        elif question_mark and len(parts) > 1:
            op_type = "equation"
        elif assignment_indices and not question_mark:
            op_type = "assignment"
        else:
            raise Exception("Shouldn't be here man")

        return op_type, parts


    def read_eval_print_loop(self):
        while True:
            try:
                input_string = input(">")
                output_string = eval(input_string)
                print(output_string)
            except (ParsingError, EvalException, MathException, TokenizationError) as e:
                print(e.message)
