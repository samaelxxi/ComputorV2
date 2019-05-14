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


class FunctionIsRecursive(EvalException):
    def __init__(self, name):
        message = "Function {} can't be defined because of recursion".format(name)
        super(FunctionIsRecursive, self).__init__(message)


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


class WrongMatrixElementType(EvalException):
    def __init__(self, elem):
        message = "Matrix can't containt elements of type {}".format(type(elem).__name__)
        super(WrongMatrixElementType, self).__init__(message)


class CantDetectUnknownVariable(EvalException):
    def __init__(self):
        message = "Can't detect unknown variable in equation"
        super(CantDetectUnknownVariable, self).__init__(message)


class IncorrectTerm(EvalException):
    def __init__(self, objs):
        message = "Term has incorrect form: ", str(objs)
        super(IncorrectTerm, self).__init__(message)


class CantSolveEquation(EvalException):
    def __init__(self, equation):
        message = "Cant solve equation of degree {}".format(equation)
        super(CantSolveEquation, self).__init__(message)


class SpecialFunctionWrongUsage(EvalException):
    def __init__(self):
        message = "Special functions can't be used in such way."
        super(SpecialFunctionWrongUsage, self).__init__(message)


class BadFunctionInput(EvalException):
    def __init__(self, func_name, input_):
        message = "Bad input to func {}: {}".format(func_name, input_)
        super(BadFunctionInput, self).__init__(message)


class MatrixIsNonInvertible(EvalException):
    def __init__(self, matrix):
        message = "Can't invert matrix:\n {}".format(matrix)
        super(MatrixIsNonInvertible, self).__init__(message)


class WrongSpecialCommandUse(EvalException):
    def __init__(self, message="Special command error"):
        super(WrongSpecialCommandUse, self).__init__(message)
