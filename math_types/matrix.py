"""Matrix class implementation"""
from exceptions.math_exceptions import WrongMatrixDimension
from exceptions.evaluation_exceptions import MatrixIsNonInvertible
from math_types import MathPrimitive
from math_types.number import Number
import operator


class Matrix(MathPrimitive):
    """
    Matrix class represents math object matrix and implements it's default behavior
        such as addition, subtraction, multiplication...
    """
    _operations = {"+": "add_to_matrix",
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

    add_to_comp_num = add_to_num
    multiply_by_comp_num = multiply_by_num

    def matrix_op_matrix_elementwise(self, other, op):
        if self.rows != other.rows or self.cols != other.cols:
            raise WrongMatrixDimension(other, self)
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(res.rows):
            for col_idx in range(res.cols):
                res.matrix[row_idx][col_idx] = op(other.matrix[row_idx][col_idx], self.matrix[row_idx][col_idx])
        return res

    def add_to_matrix(self, other):
        return self.matrix_op_matrix_elementwise(other, operator.add)

    def subtract_from_matrix(self, other):
        return self.matrix_op_matrix_elementwise(other, operator.sub)

    def multiply_by_matrix(self, other):
        return self.matrix_op_matrix_elementwise(other, operator.mul)

    def divide_matrix(self, other):
        return self.matrix_op_matrix_elementwise(other, operator.truediv)

    def modulo_matrix(self, other):
        return self.matrix_op_matrix_elementwise(other, operator.mod)

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

    def invert_matrix(self):
        if self.rows != self.cols:
            raise MatrixIsNonInvertible(self)
        n = self.rows
        matrix = Matrix(self.rows, self.cols, [row[:] for row in self.matrix])
        inverted = Matrix(n, n, [[Number(0.0) if i != j else Number(1.0) for i in range(n)] for j in range(n)])

        self._forward_elimination(matrix, inverted)
        self._backward_elimination(matrix, inverted)

        return inverted

    def transpose_matrix(self):
        transposed = Matrix(self.cols, self.rows, [[None for _ in range(self.rows)] for _ in range(self.cols)])
        for i in range(self.cols):
            for j in range(self.rows):
                transposed.matrix[i][j] = self.matrix[j][i]

        return transposed

    def _forward_elimination(self, matrix, inverted):
        n = matrix.rows
        for col_idx in range(n-1):
            cur_row = matrix.matrix[col_idx]
            if cur_row[col_idx] == Number(0):
                non_zero_row = self._find_next_nonzero_row(matrix, col_idx, col_idx+1)
                if non_zero_row is None:
                    raise MatrixIsNonInvertible(matrix)
                matrix.matrix[cur_row], matrix.matrix[non_zero_row] = matrix.matrix[non_zero_row], matrix.matrix[cur_row]

            for row_idx in range(col_idx+1, n):
                coef = matrix.matrix[row_idx][col_idx] / cur_row[col_idx]

                mult_row = [elem * coef for elem in cur_row]
                matrix.matrix[row_idx] = [matrix.matrix[row_idx][i] - mult_row[i] for i in range(n)]

                mult_row = [elem * coef for elem in inverted.matrix[col_idx]]
                inverted.matrix[row_idx] = [inverted.matrix[row_idx][i] - mult_row[i] for i in range(n)]
        if matrix.matrix[n-1][n-1] == Number(0):
            raise MatrixIsNonInvertible(matrix)

    def _backward_elimination(self, matrix, inverted):
        n = matrix.rows
        for row_idx in range(n-1, -1, -1):
            coef = Number(1) / matrix.matrix[row_idx][row_idx]
            inverted.matrix[row_idx] = [elem * coef for elem in inverted.matrix[row_idx]]

            if row_idx == 0:
                break
            coef = matrix.matrix[row_idx-1][row_idx]
            for col_idx in range(n):
                inverted.matrix[row_idx-1][col_idx] -= inverted.matrix[row_idx][col_idx] * coef

    def _find_next_nonzero_row(self, matrix, col_idx, row_idx):
        n = matrix.rows
        for i in range(row_idx, n):
            if matrix.matrix[i][col_idx] != Number(0):
                return i
        return None
