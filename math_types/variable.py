"""Variable class implementation"""
from math_types import AbstractMathType
from typing import Optional


class Variable(AbstractMathType):
    """
    Variable class
    """
    def __init__(self, name: str, val=Optional[AbstractMathType]):
        """
        :param name: name of variable(would be lowercased)
        :param val: variable value(None by default)
        """
        self.name = name.lower()
        self.val = val

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    __repr__ = __str__
