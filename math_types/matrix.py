"""Matrix class implementation"""
from exceptions.math_exceptions import OperationIsNotSupported, WrongMatrixDimension
from math_types import MathPrimitive
import operator


class Matrix(MathPrimitive):
    """
    Matrix class represents math object matrix and implements it's default behavior
        such as addition, subtraction, multiplication...
    """
    operations = {"+": "add_to_matrix",
                  "-": "subtract_from_matrix",
                  "*": "multiply_by_matrix",
                  "/": "divide_matrix",
                  "^": "power_matrix",
                  "%": "modulo_matrix",
                  "**": "matmul"}

    def __init__(self, rows, cols, matrix):
        """
        :param rows: number of rows
        :param cols: number of columns
        :param matrix: matrix as list of lists
        """
        self.rows = rows
        self.cols = cols
        self.matrix = matrix

    def __eq__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __str__(self):
        rows = []
        for row in self.matrix:
            str_row = "[ " + ", ".join(str(elem) for elem in row) + " ]"
            rows.append(str_row)
        return "\n".join(rows)

    __repr__ = __str__

    def add_to_num(self, other):
        res = Matrix(self.rows, self.cols, [row[:] for row in self.matrix])
        for row_idx in range(self.rows):
            for col_idx in range(self.cols):
                res.matrix[row_idx][col_idx] += other
        return res

    def multiply_by_num(self, other):
        res = Matrix(self.rows, self.cols, [row[:] for row in self.matrix])
        for row_idx in range(self.rows):
            for col_idx in range(self.cols):
                res.matrix[row_idx][col_idx] *= other
        return res

    def matrix_elementwise_op(self, other, op):
        if self.rows != other.rows or self.cols != other.cols:
            raise WrongMatrixDimension(other, self)
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(res.rows):
            for col_idx in range(res.cols):
                res.matrix[row_idx][col_idx] = op(other.matrix[row_idx][col_idx], self.matrix[row_idx][col_idx])
        return res

    def add_to_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.add)

    def subtract_from_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.sub)

    def multiply_by_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.mul)

    def divide_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.truediv)

    def modulo_matrix(self, other):
        return self.matrix_elementwise_op(other, operator.mod)

    def matmul(self, other):
        left, right = other, self

        if left.cols != right.rows:
            raise WrongMatrixDimension(left, right)

        res = Matrix(left.rows, right.cols, [[None for _ in range(right.cols)] for _ in range(left.rows)])
        for row in range(res.rows):
            for col in range(res.cols):
                res.matrix[row][col] = self._calc_matrix_matmul_elem(left, right, row, col)

        return res

    @staticmethod
    def _calc_matrix_matmul_elem(left, right, row, col):
        res = None
        for i in range(left.cols):
            cur_prod = left.matrix[row][i] * right.matrix[i][col]
            res = cur_prod if res is None else res + cur_prod

        return res
