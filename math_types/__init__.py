"""This package contains all math types used in project"""

from math_types.math_type import AbstractMathType, MathPrimitive
from math_types.complex_number import ComplexNumber
from math_types.equation import Equation
from math_types.function import Function
from math_types.matrix import Matrix
from math_types.number import Number
from math_types.variable import Variable
from math_types.operator import Operator
from math_types.expression import Expression

MATH_TYPES = [Number, ComplexNumber, Matrix, Variable, Function]