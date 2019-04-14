"""Number class implementation"""

from math import isclose


class Number:
    """
    Implementation of number and it's operations
    Number may interact with other ComplexNumber or Number
    """
    def __init__(self, val):
        """
        :param val: value of number(int or float)
        """
        self.val = val

    def __eq__(self, other):
        return isclose(self.val, other.val)

    def __str__(self):
        return str(self.val)

    __repr__ = __str__
