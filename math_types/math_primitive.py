from abc import abstractmethod
from exceptions.math_exceptions import OperationIsNotSupported


class MathPrimitive:
    """
    Abstract class for math objects such as Number, Complex Number and Complex Number
    They are united by behavior, which allows operations between any pair of this types
    They should implement addition, subtraction, multiplication, division, modulo,
    power and matrix multiplication if it's possible.
    Type matching is implemented via duck typing. Each class should
    have operation dictionary, where key it's math operand and value it's
    name of the method that other operand should(or shouldn't implement).
    This methods should be reversed, so when it's called with (self, other),
    self is actually right operand and other is left.
    Then, during math operations, left operand checks if right operand has
    required function to be operated with current class and calls it or throws exception
    """

    @property
    @abstractmethod
    def _operations(self):
        raise NotImplementedError

    def __add__(self, other):
        try:
            other_op_method = getattr(other, self._operations["+"])
            return other_op_method(self)
        except AttributeError:
            raise OperationIsNotSupported(self.__class__, "+", type(other))

    def __sub__(self, other):
        try:
            other_op_method = getattr(other, self._operations["-"])
            return other_op_method(self)
        except AttributeError:
            raise OperationIsNotSupported(self.__class__, "-", type(other))

    def __mul__(self, other):
        try:
            other_op_method = getattr(other, self._operations["*"])
            return other_op_method(self)
        except AttributeError:
            raise OperationIsNotSupported(self.__class__, "*", type(other))

    def __truediv__(self, other):
        try:
            other_op_method = getattr(other, self._operations["/"])
            return other_op_method(self)
        except AttributeError:
            raise OperationIsNotSupported(self.__class__, "/", type(other))

    def __xor__(self, other):
        try:
            other_op_method = getattr(other, self._operations["^"])
            return other_op_method(self)
        except AttributeError:
            raise OperationIsNotSupported(self.__class__, "^", type(other))

    def __mod__(self, other):
        try:
            other_op_method = getattr(other, self._operations["%"])
            return other_op_method(self)
        except AttributeError:
            raise OperationIsNotSupported(self.__class__, "%", type(other))

    def __pow__(self, other):
        try:
            other_op_method = getattr(other, self._operations["**"])
            return other_op_method(self)
        except AttributeError:
            raise OperationIsNotSupported(self.__class__, "**", type(other))
