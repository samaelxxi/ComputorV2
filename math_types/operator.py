"""Operator class implementation"""


class Operator:
    def __init__(self, op):
        """
        :param op: string which represents operator symbol
        """
        self.op = op

    def __eq__(self, other):
        return self.op == other.op

    def __str__(self):
        return self.op

    __repr__ = __str__
