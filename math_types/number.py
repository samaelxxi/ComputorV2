"""Number class implementation"""

from math import isclose
from exceptions.math_exceptions import OperationIsNotSupported
from math_types import ComplexNumber, Matrix


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
            return other.add_to_num(self)
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

    def add_to_num(self, other):
        return Number(other.val + self.val)

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

    def add_to_comp_num(self, other):
        return ComplexNumber(self.val + other.real, other.imag)

    def subtract_from_comp_num(self, other):
        return ComplexNumber(other.real - self.val, other.imag)

    def multiply_by_comp_num(self, other):
        return ComplexNumber(self.val * other.real, self.val * other.imag)

    def divide_comp_num(self, other):
        return ComplexNumber(other.real / self.val, other.imag / self.val)

    def power_comp_num(self, other):
        if self.val <= 0 or not isclose(self.val, int(self.val)):
            raise OperationIsNotSupported(Number, "^", type(other))
        res = other
        for i in range(self.val-1):
            res = res * res
        return res

    def add_to_matrix(self, other):
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] + self
        return res

    def subtract_from_matrix(self, other):
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] - self
        return res

    def multiply_by_matrix(self, other):
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] * self
        return res

    def divide_matrix(self, other):
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] / self
        return res

    def modulo_matrix(self, other):
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] % self
        return res

    def power_matrix(self, other):
        if self.val <= 0 or not isclose(self.val, int(self.val)):
            raise OperationIsNotSupported(Number, "^", type(other))
        res = other
        for i in range(self.val-1):
            res = res ** other
        return res

    def __str__(self):
        return str(self.val)

    __repr__ = __str__
