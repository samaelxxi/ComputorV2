"""Complex number class implementation"""

import operator
from math import isclose
from exceptions.math_exceptions import ZeroDivisionError
from math_types import MathPrimitive
from math_types.matrix import Matrix


class ComplexNumber(MathPrimitive):
    """
    Implementation of complex number and it's operations
    ComplexNumber may interact with other ComplexNumber, Number or Matrix
    """
    _operations = {"+": "add_to_comp_num",
                   "-": "subtract_from_comp_num",
                   "*": "multiply_by_comp_num",
                   "/": "divide_comp_num",
                   "^": "power_comp_num",
                   "%": "modulo_comp_num",
                   "**": "matmul_comp_num"}

    def __init__(self, real: float, imag: float):
        """
        :param real: number for real part
        :param imag: number for imaginary part of number
        """
        self.real = real
        self.imag = imag

    def __eq__(self, other):
        return isclose(self.real, other.real) and isclose(self.imag, other.imag)

    def __str__(self):
        return "{} {} {}i".format(self.real, "+" if self.imag > 0 else "-", abs(self.imag))

    __repr__ = __str__

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
        if isclose(denom, 0):
            raise ZeroDivisionError(other, self)
        real = (self.real * other.real + self.imag * other.imag) / denom
        imag = (self.real * other.imag - self.imag * other.real) / denom
        return ComplexNumber(real, imag)

    def matrix_elementwise_op(self, matrix, op):
        res = Matrix(matrix.rows, matrix.cols, [row[:] for row in matrix.matrix])
        for row_idx in range(res.rows):
            for col_idx in range(res.cols):
                res.matrix[row_idx][col_idx] = op(res.matrix[row_idx][col_idx], self)
        return res

    def add_to_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.add)

    def subtract_from_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.sub)

    def multiply_by_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.mul)

    def divide_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.truediv)
