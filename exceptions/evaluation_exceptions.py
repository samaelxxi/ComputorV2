"""Module for expression evaluations errors"""


class EvalException(Exception):
    """Basic math exception"""


class TooManyAssignments(EvalException):
    def __init__(self):
        message = "Only one assignment operator per line is allowed"
        super(TooManyAssignments, self).__init__(message)


class VariableNotExists(EvalException):
    def __init__(self, name):
        message = "Variable {} doesn't exists".format(name)
        super(VariableNotExists, self).__init__(message)


class FunctionNotExists(EvalException):
    def __init__(self, name):
        message = "Function {} doesn't exists".format(name)
        super(FunctionNotExists, self).__init__(message)


class NoExpectedOperand(EvalException):
    def __init__(self, name):
        message = "No operand for operation {} ".format(name)
        super(NoExpectedOperand, self).__init__(message)