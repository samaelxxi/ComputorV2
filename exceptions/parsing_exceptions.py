"""
Exceptions related to parsing stage of program
"""


class TokenizationError(Exception):
    """Basic exception for tokenization errors"""


class UnknownToken(TokenizationError):
    """Exception for unknown tokens"""
    def __init__(self, token):
        message = "Can't recognize token '{}'".format(token)
        super(UnknownToken, self).__init__(message)
