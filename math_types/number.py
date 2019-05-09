"""Number class implementation"""

from math import isclose
from exceptions.math_exceptions import OperationIsNotSupported, ZeroDivisionError, PowerError
from math_types import ComplexNumber, MathPrimitive
import operator


class Number(MathPrimitive):
    """
    Implementation of number and it's operations
    Number may interact with other ComplexNumber or Number
    """
    _operations = {"+": "add_to_num",
                  "-": "subtract_from_num",
                  "*": "multiply_by_num",
                  "/": "divide_num",
                  "^": "power_num",
                  "%": "modulo_num",
                  "**": "matmul_num"}

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

    def add_to_num(self, other):
        return Number(other.val + self.val)

    def subtract_from_num(self, other):
        return Number(other.val - self.val)

    def multiply_by_num(self, other):
        return Number(self.val * other.val)

    def divide_num(self, other):
        if isclose(self.val, 0):
            raise ZeroDivisionError(other, self)
        return Number(other.val / self.val)

    def power_num(self, other):
        try:
            res = other.val ** self.val
        except OverflowError:
            raise PowerError(other, self)
        if type(res) == complex:
            raise PowerError(other, self)
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
        if isclose(self.val, 0):
            raise ZeroDivisionError(other, self)
        return ComplexNumber(other.real / self.val, other.imag / self.val)

    def power_comp_num(self, other):
        if self.val <= 0 or not isclose(self.val, int(self.val)):
            raise OperationIsNotSupported(Number, "^", type(other))
        res = other
        for i in range(int(self.val-1)):
            res = res * res
        return res

    def matrix_elementwise_op(self, matrix, op):
        from math_types import Matrix
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
        if isclose(self.val, 0):
            raise ZeroDivisionError(other, self)
        return self.matrix_elementwise_op(other, operator.truediv)

    def modulo_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.mod)

    def power_matrix(self, other):
        if self.val <= 0 or not isclose(self.val, int(self.val)):
            raise OperationIsNotSupported(Number, "^", type(other))
        res = other
        for i in range(int(self.val-1)):
            res = res ** other
        return res
