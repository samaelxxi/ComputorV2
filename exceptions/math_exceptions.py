"""Module for math errors"""


class MathException(Exception):
    """Basic math exception"""


class OperationIsNotSupported(MathException):
    def __init__(self, type1, op, type2):
        message = "Operation {} between {} and {} is not supported".format(type1, op, type2)
        super(OperationIsNotSupported, self).__init__(message)


class WrongMatrixDimension(MathException):
    def __init__(self, m1, m2):
        message = "Matrix with dimension {}x{} doesn't match matrix with dimension {}x{}".format(m1.rows, m1.cols,
                                                                                                 m2.rows, m2.cols)
        super(WrongMatrixDimension, self).__init__(message)