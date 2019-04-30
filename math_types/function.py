"""Function class implementation"""
from math_types import Variable


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
        self.body = body

    def __eq__(self, other):
        return self.name == other.name and self.input == other.input

    def __str__(self):
        if self.body is not None:
            return str(self.body)
        else:
            return "{}({})".format(self.name, self.input)

    __repr__ = __str__

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
