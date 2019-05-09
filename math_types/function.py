"""Function class implementation"""
from math_types import Variable, Number, Matrix
from exceptions.evaluation_exceptions import SpecialFunctionWrongUsage, BadFunctionInput, MatrixIsNonInvertible
import abc


class Function:

    """
    Function class could be used to store function calls or functions as whole
    If function represents only function call, it's body is None and input is Expression
    Else if function is defined as math object, it's body is Expression, and input is Variable which
        is used in function body
    """
    def __init__(self, name, input_, body=None):
        """
        :param name: function name
        :param input_: function input(values between brackets). Should be Number, ComplexNumber, Variable or Expression
        :param body: function body, if it's defined, otherwise None
        """
        self.name = name
        self.input = input_
        self._body = body

    def __eq__(self, other):
        return self.name == other.name and self.input == other.input

    def __str__(self):
        if self.body is not None:
            return str(self.body)
        else:
            return "{}({})".format(self.name, self.input)

    __repr__ = __str__

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, item):
        self._body = item

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


class SpecialFunction(Function):
    def __init__(self, name, eval_func):
        super().__init__(name, Variable("x"))
        self._body = None

    @property
    def body(self):
        raise SpecialFunctionWrongUsage()

    @abc.abstractmethod
    def evaluate(self, func_input, variables, functions):
        pass


class SpecialMathFunction(SpecialFunction):
    def __init__(self, name, eval_func):
        super().__init__(name, Variable("x"))
        self.eval_func = eval_func

    def evaluate(self, func_input, variables, functions):
        func_input_value = func_input.evaluate(variables, functions)
        if not isinstance(func_input_value, Number):
            raise BadFunctionInput(self.name, func_input_value)
        try:
            return self.eval_func(func_input_value.val)
        except (ValueError, OverflowError) as e:
            raise BadFunctionInput(self.name, func_input_value)


class MatrixInversionFunc(SpecialFunction):
    def __init__(self, name):
        super().__init__(name, Variable("x"))

    def evaluate(self, func_input, variables, functions):
        matrix = func_input.evaluate(variables, functions)
        if not isinstance(matrix, Matrix):
            raise BadFunctionInput(self.name, matrix)
        if not all(isinstance(matrix.matrix[i][j], Number) for i in range(matrix.rows) for j in range(matrix.cols)):
            raise BadFunctionInput(self.name, matrix)
        inverted = matrix.invert_matrix()
        return inverted


class MatrixTransposeFunc(SpecialFunction):
    def __init__(self, name):
        super().__init__(name, Variable("x"))

    def evaluate(self, func_input, variables, functions):
        matrix = func_input.evaluate(variables, functions)
        if not isinstance(matrix, Matrix):
            raise BadFunctionInput(self.name, matrix)
        transposed = matrix.transpose_matrix()
        return transposed


class SpecialCommand(SpecialFunction):
    pass