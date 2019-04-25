"""Matrix class implementation"""
from exceptions.math_exceptions import OperationIsNotSupported, WrongMatrixDimension

class Matrix:
    """
    Matrix class represents math object matrix and implements it's default behavior
        such as addition, subtraction, multiplication...
    """
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

    def __add__(self, other):
        try:
            return other.add_to_matrix(self)
        except AttributeError:
            raise OperationIsNotSupported(Matrix, "+", type(other))

    def __sub__(self, other):
        try:
            return other.subtract_from_matrix(self)
        except AttributeError:
            raise OperationIsNotSupported(Matrix, "-", type(other))

    def __mul__(self, other):
        try:
            return other.multiply_by_matrix(self)
        except AttributeError:
            raise OperationIsNotSupported(Matrix, "*", type(other))

    def __truediv__(self, other):
        try:
            return other.divide_matrix(self)
        except AttributeError:
            raise OperationIsNotSupported(Matrix, "/", type(other))

    def __xor__(self, other):
        try:
            return other.power_matrix(self)
        except AttributeError:
            raise OperationIsNotSupported(Matrix, "^", type(other))

    def __mod__(self, other):
        try:
            return other.modulo_matrix(self)
        except AttributeError:
            raise OperationIsNotSupported(Matrix, "%", type(other))

    def __pow__(self, other):
        try:
            return other.matmul(self)
        except AttributeError:
            raise OperationIsNotSupported(Matrix, "**", type(other))

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

    def add_to_matrix(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise WrongMatrixDimension(other, self)
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] + self.matrix[row_idx][col_idx]
        return res

    def subtract_from_matrix(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise WrongMatrixDimension(other, self)
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] - self.matrix[row_idx][col_idx]
        return res

    def multiply_by_matrix(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise WrongMatrixDimension(other, self)
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] * self.matrix[row_idx][col_idx]
        return res

    def divide_matrix(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise WrongMatrixDimension(other, self)
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] / self.matrix[row_idx][col_idx]
        return res

    def modulo_matrix(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise WrongMatrixDimension(other, self)
        res = Matrix(other.rows, other.cols, [row[:] for row in other.matrix])
        for row_idx in range(other.rows):
            for col_idx in range(other.cols):
                res.matrix[row_idx][col_idx] = other.matrix[row_idx][col_idx] % self
        return res

    def matmul(self, other):
        left, right = other, self

        if left.cols != right.rows:
            raise WrongMatrixDimension(left, right)

        res = Matrix(left.rows, right.cols, [[None for _ in range(right.cols)] for _ in range(left.rows)])
        for row in range(res.rows):
            for col in range(res.cols):
                res.matrix[row][col] = self._calc_matrix_elem(left, right, row, col)

        return res

    @staticmethod
    def _calc_matrix_elem(left, right, row, col):
        res = None
        for i in range(left.cols):
            cur_prod = left.matrix[row][i] * right.matrix[i][col]
            res = cur_prod if res is None else res + cur_prod

        return res

    __repr__ = __str__
