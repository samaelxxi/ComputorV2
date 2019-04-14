"""Complex number class implementation"""

from math import isclose


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
