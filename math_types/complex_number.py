"""Complex number class implementation"""

from math import isclose
from exceptions.math_exceptions import OperationIsNotSupported


class ComplexNumber:
    """
    Implementation of complex number and it's operations
    ComplexNumber may interact with other ComplexNumber or Number
    """
    def __init__(self, real, imag):
        """
        :param real: number for real part
        :param imag: number for imaginary part of number
        """
        self.real = real
        self.imag = imag

    def __eq__(self, other):
        return isclose(self.real, other.real) and isclose(self.imag, other.imag)

    def __add__(self, other):
        try:
            return other.add_to_comp_num(self)
        except AttributeError:
            raise OperationIsNotSupported(ComplexNumber, "+", type(other))

    def __sub__(self, other):
        try:
            return other.subtract_from_comp_num(self)
        except AttributeError:
            raise OperationIsNotSupported(ComplexNumber, "-", type(other))

    def __mul__(self, other):
        try:
            return other.multiply_by_comp_num(self)
        except AttributeError:
            raise OperationIsNotSupported(ComplexNumber, "*", type(other))

    def __truediv__(self, other):
        try:
            return other.divide_comp_num(self)
        except AttributeError:
            raise OperationIsNotSupported(ComplexNumber, "*", type(other))

    def __xor__(self, other):
        try:
            return other.power_comp_num(self)
        except AttributeError:
            raise OperationIsNotSupported(ComplexNumber, "*", type(other))

    def __mod__(self, other):
        try:
            return other.modulo_comp_num(self)
        except AttributeError:
            raise OperationIsNotSupported(ComplexNumber, "*", type(other))

    def add_to_num(self, other):
        return ComplexNumber(self.real + other.val, self.imag)

    def subtract_from_num(self, other):
        return ComplexNumber(other.val - self.real, -self.imag)

    def multiply_by_num(self, other):
        return ComplexNumber(self.real * other.val, self.imag * other.val)

    def divide_num(self, other):
        return ComplexNumber(other.val, 0) / self

    def add_to_comp_num(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def subtract_from_comp_num(self, other):
        return ComplexNumber(other.real - self.real, other.imag - self.imag)

    def multiply_by_comp_num(self, other):
        real = self.real * other.real - self.imag * other.imag
        imag = self.real * other.imag + self.imag * other.real
        return ComplexNumber(real, imag)

    def divide_comp_num(self, other):
        denom = self.real ** 2 + self.imag ** 2
        real = (self.real * other.real + self.imag * other.imag) / denom
        imag = (self.real * other.imag - self.imag * other.real) / denom
        return ComplexNumber(real, imag)
