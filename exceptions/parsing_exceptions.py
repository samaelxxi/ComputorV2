"""
Exceptions related to parsing stage of program
"""


class TokenizationError(Exception):
    """Basic exception for tokenization errors"""


class ParsingError(Exception):
    """Basic exception for parsing errors"""


class UnknownToken(TokenizationError):
    def __init__(self, token):
        message = "Can't recognize token '{}'".format(token)
        super(UnknownToken, self).__init__(message)


class BracketsMismatch(ParsingError):
    def __init__(self, open_br, close_br):
        message = "Brackets mismatch: {} and {}".format(open_br, close_br)
        super(BracketsMismatch, self).__init__(message)


class NoClosingBracket(ParsingError):
    def __init__(self, bracket):
        message = "No closing bracket for {}".format(bracket)
        super(NoClosingBracket, self).__init__(message)

class ExtraBracket(ParsingError):
    def __init__(self, bracket):
        message = "Extra bracket: {}".format(bracket)
        super(ExtraBracket, self).__init__(message)

class BadNumber(ParsingError):
    def __init__(self, token):
        message = "Can't parse number {}".format(token)
        super(BadNumber, self).__init__(message)


class MatrixDiffElems(ParsingError):
    def __init__(self):
        message = "Matrix has different number of elems in rows"
        super(MatrixDiffElems, self).__init__(message)


class EmptyMatrix(ParsingError):
    def __init__(self):
        message = "Matrix can't be empty"
        super(EmptyMatrix, self).__init__(message)


class UnexpectedToken(ParsingError):
    def __init__(self, token):
        message = "Unexpected token: {}".format(str(token))
        super(UnexpectedToken, self).__init__(message)