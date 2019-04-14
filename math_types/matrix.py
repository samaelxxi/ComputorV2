"""Matrix class implementation"""

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
        return "/n".join(rows)

    __repr__ = __str__
