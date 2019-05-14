"""Function class implementation"""
from math_types import Variable, Number, Matrix
from exceptions.evaluation_exceptions import SpecialFunctionWrongUsage, BadFunctionInput
import abc


class AFunction(abc.ABC):
    def __init__(self, name, input_, body=None):
        """
        :param name: function name
        :param input_: function input(values between brackets). Should be Number, ComplexNumber, Variable or Expression
        :param body: function body, if it's defined, otherwise None
        """
        self.name = name
        self.input = input_
        self._body = body

    def __str__(self):
        if self.body is not None:
            return "{}({}) = {}".format(self.name, self.input, str(self.body))
        else:
            return "{}({})".format(self.name, self.input)

    __repr__ = __str__

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, item):
        self._body = item


class UserDefinedFunction(AFunction):
    """
    Function class could be used to store function calls or functions as whole
    If function represents only function call, it's body is None and input is Expression
    Else if function is defined as math object, it's body is Expression, and input is Variable which
        is used in function body
    """
    def __init__(self, name, input_, body=None):
        super().__init__(name, input_, body)

    def __eq__(self, other):
        return self.name == other.name and self.input == other.input

    def evaluate(self, func_input, variables, functions):
        """
        Evaluates self

        :param func_input: expression which is used for input
        :param variables: dict of defined variables
        :param functions: dict of defined functions
        :return: evaluation result (MathPrimitive)
        """
        if self.body is None:
            raise Exception("Shouldn't be here")

        func_var_name = self.input.name
        func_input_value = func_input.evaluate(variables, functions)

        res = self.body.evaluate({func_var_name: Variable(func_var_name, func_input_value)},
                                 functions)

        return res


class SpecialFunction(AFunction):
    """
    Special functions represents some function which couldn't be defined by user,
    but could be defined inside program. Such functions have implementation, but it
    couldn't be accessed, so any attempt to access body attribute(like, during equation solving)
    would raise exception.
    Also, such functions usually expect arguments with defined type, so it has
    argument check before execution
    """
    def __init__(self, name, eval_func, expected_types):
        """
        :param name: function name
        :param eval_func: function which will be called during evaluation
        :param expected_types: tuple of accessible argument types
        """
        super().__init__(name, Variable("x"))
        self.eval_func = eval_func
        self.expected_types = expected_types

    def __str__(self):
        return "{}({})".format(self.name, self.input)

    @property
    def body(self):
        raise SpecialFunctionWrongUsage()

    def evaluate(self, func_input, variables, functions):
        func_input_value = func_input.evaluate(variables, functions)
        if not isinstance(func_input_value, self.expected_types):
            raise BadFunctionInput(self.name, func_input_value)
        return self.eval_func(func_input_value)


class SpecialNumericFunction(SpecialFunction):
    def __init__(self, name, eval_func):

        def eval(var):
            try:
                return eval_func(var.val)
            except (ValueError, OverflowError) as e:
                raise BadFunctionInput(name, var)

        super().__init__(name, eval, (Number,))


class MatrixInversionFunc(SpecialFunction):
    def __init__(self, name):

        def eval(matrix):
            if not all(isinstance(matrix.matrix[i][j], Number) for i in range(matrix.rows) for j in range(matrix.cols)):
                raise BadFunctionInput(self.name, matrix)
            inverted = matrix.invert_matrix()
            return inverted

        super().__init__(name, eval, (Matrix,))


class MatrixTransposeFunc(SpecialFunction):
    def __init__(self, name):

        def eval(matrix):
            return matrix.transpose_matrix()

        super().__init__(name, eval, (Matrix,))


class SpecialCommand(AFunction):
    def __init__(self, name, eval_func):
        super().__init__(name, None, None)
        self.eval_func = eval_func

    def evaluate(self, func_input, variables, functions):
        return self.eval_func(func_input.body, variables, functions)
