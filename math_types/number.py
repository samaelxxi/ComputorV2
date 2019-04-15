"""Number class implementation"""

from math import isclose
from exceptions.math_exceptions import OperationIsNotSupported
from math_types import ComplexNumber


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

    def __add__(self, other):
        try:
            return other.sum_with_num(self)
        except AttributeError:
            raise OperationIsNotSupported(Number, "+", type(other))

    def __sub__(self, other):
        try:
            return other.subtract_from_num(self)
        except AttributeError:
            raise OperationIsNotSupported(Number, "-", type(other))

    def __mul__(self, other):
        try:
            return other.multiply_by_num(self)
        except AttributeError:
            raise OperationIsNotSupported(Number, "*", type(other))

    def __truediv__(self, other):
        try:
            return other.divide_num(self)
        except AttributeError:
            raise OperationIsNotSupported(Number, "/", type(other))

    def __xor__(self, other):
        try:
            return other.power_num(self)
        except AttributeError:
            raise OperationIsNotSupported(Number, "^", type(other))

    def __mod__(self, other):
        try:
            return other.modulo_num(self)
        except AttributeError:
            raise OperationIsNotSupported(Number, "%", type(other))

    def sum_with_num(self, other):
        return Number(self.val + other.val)

    def subtract_from_num(self, other):
        return Number(other.val - self.val)

    def multiply_by_num(self, other):
        return Number(self.val * other.val)

    def divide_num(self, other):
        return Number(other.val / self.val)

    def power_num(self, other):
        return Number(other.val ** self.val)

    def modulo_num(self, other):
        return Number(other.val % self.val)

    def sum_with_comp_num(self, other):
        return ComplexNumber(self.val + other.real, other.imag)

    def subtract_from_comp_num(self, other):
        return ComplexNumber(other.real - self.val, other.imag)

    def multiply_by_comp_num(self, other):
        return ComplexNumber(self.val * other.real, self.val * other.imag)

    def divide_comp_num(self, other):
        return ComplexNumber(other.real / self.val, other.imag / self.val)

    def power_comp_num(self, other):
        if self.val < 0 or not isclose(self.val, int(self.val)):
            raise OperationIsNotSupported(Number, "^", type(other))
        res = other
        for i in range(self.val-1):
            res = res * res
        return res

    def __str__(self):
        return str(self.val)

    __repr__ = __str__
