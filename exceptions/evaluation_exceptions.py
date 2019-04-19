"""Module for expression evaluations errors"""


class EvalException(Exception):
    """Basic math exception"""


class TooManyAssignments(EvalException):
    def __init__(self):
        message = "Only one assignment operator per line is allowed"
        super(TooManyAssignments, self).__init__(message)


class VariableNotDefined(EvalException):
    def __init__(self, name):
        message = "Variable {} isn't defined".format(name)
        super(VariableNotDefined, self).__init__(message)


class FunctionNotExists(EvalException):
    def __init__(self, name):
        message = "Function {} doesn't exists".format(name)
        super(FunctionNotExists, self).__init__(message)


class NoExpectedOperand(EvalException):
    def __init__(self, name):
        message = "No operand for operation {} ".format(name)
        super(NoExpectedOperand, self).__init__(message)


class WrongAssingmentLeftPart(EvalException):
    def __init__(self, left):
        message = "Can't assign to {}".format(type(left).__name__)
        super(WrongAssingmentLeftPart, self).__init__(message)


class ExpressionIsNotValid(EvalException):
    def __init__(self, expr):
        message = "Expression is not valid: " + " ".join(str(obj) for obj in expr)
        super(ExpressionIsNotValid, self).__init__(message)
