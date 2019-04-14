"""Function class implementation"""


class Function:
    """
    Function class could be used to store function calls or functions as whole
    If function represents only function call, it's body is None
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
