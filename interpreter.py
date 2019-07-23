from exceptions import MathException, ParsingError, EvalException, TokenizationError
from exceptions.parsing_exceptions import UnexpectedToken
from exceptions.evaluation_exceptions import TooManyAssignments, WrongAssingmentLeftPart, \
    WrongSpecialCommandUse, FunctionIsRecursive, FunctionNotExists
from typing import Tuple, List
from parsing.tokenizer import Tokenizer
from parsing.parser import Parser
from math_types import Operator, AFunction, Variable, Expression, Equation, UserDefinedFunction
from math_types.function import MatrixInversionFunc, MatrixTransposeFunc, SpecialNumericFunction
from consts import DEFINED_VARS, DEFINED_FUNCS, SPECIAL_COMMANDS


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

    Predefined math functions: sin, cos, tan, log, abs, sqrt, exp
    Predefined matrix functions: inv, transp
    Predefined special commands: vars, funcs, plot, linreg
    """
    def __init__(self):
        self._variables = self._init_predefined_variables()
        self._functions = self._init_predefined_functions()

        self._parser = Parser()
        self._tokenizer = Tokenizer()

    def _init_predefined_variables(self):
        variables = {}
        for var_name, var_val in DEFINED_VARS.items():
            variables[var_name] = Variable(var_name, var_val)
        return variables

    def _init_predefined_functions(self):
        functions = {}
        for func_name, func in DEFINED_FUNCS.items():
            func_obj = SpecialNumericFunction(func_name, func)
            functions[func_name] = func_obj

        functions["inv"] = MatrixInversionFunc("inv")
        functions["transp"] = MatrixTransposeFunc("transp")

        return functions

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
                if output_string is not None:
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
        elif op_type == "special":
            spec_comm = SPECIAL_COMMANDS[left[0].name]
            eval_res = spec_comm.evaluate(left[0].input, self._variables, self._functions)
        elif op_type == "print_func":  # kostyl
            if left[0].name not in self._functions:
                raise FunctionNotExists(left[0].name)
            f = self._functions[left[0].name]
            return str(f.body)
        else:
            raise Exception("Shouldn't be here man")

        return str(eval_res) if eval_res else None

    def _make_assignment(self, left: List, right: List) -> str:
        """
        Tries to assign right part to left

        :param left: list of objects on left part of assignment
        :param right: list of objects on right part of assignment
        :return: string which describes assignment
        """
        if len(left) != 1:
            raise WrongAssingmentLeftPart(left[0] if len(left) else None)
        left = left[0]

        if isinstance(left, Variable):
            right_part_evaluated = Expression(right).evaluate(self._variables, self._functions)
            left.val = right_part_evaluated
            self._variables[left.name] = left
            output = right_part_evaluated

        elif isinstance(left, AFunction):
            if len(left.input) != 1 or not isinstance(left.input.body[0], Variable):
                raise WrongAssingmentLeftPart(left.input)
            left_input_variable = left.input.body[0]
            func_body = Expression(right)
            if self._func_body_is_recursive(left.name, right):
                raise FunctionIsRecursive(left.name)
            func_body.evaluate_variables(self._variables, exceptions=[left_input_variable])
            left.body = func_body
            left.input = left_input_variable
            self._functions[left.name] = left
            output = str(left)

        else:
            raise WrongAssingmentLeftPart(left)

        return output

    def _func_body_is_recursive(self, func_name, func_body):
        """
        Checks if func_body contains any calls to func_name, including one that nested

        :param func_name: name of checked function
        :param func_body: list of objects
        :return: True or False
        """
        for obj in func_body:
            if isinstance(obj, AFunction):
                if obj.name == func_name:
                    return True
                if self._func_body_is_recursive(func_name, obj.input.body):
                    return True
                if obj.name in self._functions and isinstance(self._functions[obj.name], UserDefinedFunction):
                    if self._func_body_is_recursive(func_name, self._functions[obj.name].body.body):
                        return True
        return False

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

        if Interpreter._is_special_command(left, right):
            op_type = "special"
        elif (question_mark and len(right) == 1 and len(left) == 1 and isinstance(left[0], AFunction) and
              len(left[0].input.body) == 1 and isinstance(left[0].input.body[0], Variable)):
            op_type = "print_func"  # stupid case for function definition printing
        elif right is None or (question_mark and len(right) == 1):
            op_type = "evaluation"   # 'expression = ?' or no assignment operator line
        elif question_mark and len(right) > 1:
            op_type = "equation"
        elif assignment_indices and not question_mark:
            op_type = "assignment"
        else:
            raise Exception("Shouldn't be here man")

        return op_type, left, right

    @staticmethod
    def _is_special_command(left, right):
        special_funcs = []
        for obj in left:
            if isinstance(obj, AFunction) and obj.name in SPECIAL_COMMANDS:
                special_funcs.append(obj)
        if special_funcs:
            if len(left) > 1 or right is not None:
                raise WrongSpecialCommandUse()
            return True
        else:
            return False
