from math_types import *
import pytest
from exceptions.math_exceptions import *


def test1():
    assert Number(1) + Number(0) == Number(1)


def test2():
    assert Number(153.5) + Number(10.789) == Number(153.5+10.789)


def test3():
    assert Number(10.789) + Number(153.5) == Number(153.5+10.789)


def test4():
    assert Number(1) - Number(0) == Number(1)


def test5():
    assert Number(10.5) - Number(3) == Number(7.5)


def test6():
    assert Number(3) - Number(10.5) == Number(-7.5)


def test7():
    assert Number(0) - Number(1234) == Number(-1234)


def test8():
    assert Number(1) * Number(0) == Number(0)


def test9():
    assert Number(42.5) * Number(0.5) == Number(21.25)


def test10():
    assert Number(10) * Number(-1) == Number(-10)


def test11():
    with pytest.raises(ZeroDivisionError):
        Number(1) / Number(0)


def test12():
    assert Number(1) / Number(0.5) == Number(2.0)


def test13():
    assert Number(42.5) / Number(2) == Number(42.5) * Number(0.5)


def test14():
    assert Number(1) ^ Number(2) == Number(1)


def test15():
    assert Number(0) ^ Number(100) == Number(0)


def test16():
    assert Number(2) ^ Number(4) == Number(16)


def test17():
    assert Number(2.46) ^ Number(4.2) == Number(2.46**4.2)


def test18():
    assert Number(2.46) % Number(2) == Number(2.46 % 2)


def test19():
    assert ComplexNumber(2.46, 9) + Number(4.2) == ComplexNumber(2.46+4.2, 9)


def test20():
    assert ComplexNumber(2, 94.2) - Number(4.2) == ComplexNumber(2-4.2, 94.2)


def test21():
    assert  Number(4.2) + ComplexNumber(2.46, 9) == ComplexNumber(2.46+4.2, 9)


def test22():
    assert Number(4.2) - ComplexNumber(2, 94.2) == ComplexNumber(4.2-2, -94.2)


def test23():
    assert Number(2) * ComplexNumber(4.2, 94.2) == ComplexNumber(2*4.2, 2*94.2)


def test24():
    assert Number(0) * ComplexNumber(4.2, 94.2) == ComplexNumber(0, 0)


def test25():
    assert ComplexNumber(4.2, 94.2) * Number(2) == ComplexNumber(2*4.2, 2*94.2)


def test26():
    assert ComplexNumber(4.2, 94.2) * Number(0) == ComplexNumber(0, 0)


def test27():
    assert Number(2) / ComplexNumber(3, -2) == ComplexNumber(6/13, 4/13)


def test28():
    assert Number(0) / ComplexNumber(4.2, 94.2) == ComplexNumber(0, 0)


def test29():
    assert ComplexNumber(4.2, 94.2) / Number(2) == ComplexNumber(4.2/2, 94.2/2)


def test30():
    with pytest.raises(ZeroDivisionError):
        ComplexNumber(4.2, 94.2) / Number(0)


def test31():
    with pytest.raises(OperationIsNotSupported):
        Number(0) % ComplexNumber(4.2, 94.2)


def test32():
    with pytest.raises(OperationIsNotSupported):
        Number(0) ^ ComplexNumber(4.2, 94.2)


def test33():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(4.2, 94.2) % Number(2)


def test34():
    assert ComplexNumber(4.2, 94.2) ^ Number(2) == ComplexNumber(4.2, 94.2) * ComplexNumber(4.2, 94.2)


def test35():
    assert ComplexNumber(4.2, 94.2) ^ Number(1) == ComplexNumber(4.2, 94.2)


def test36():
    assert ComplexNumber(2, 3.1) * ComplexNumber(3, 1.2) == ComplexNumber(2.28, 11.7)


def test37():
    assert ComplexNumber(2, 3.1) * ComplexNumber(0, 1.2) == ComplexNumber(-3.72, 2.4)


def test38():
    assert ComplexNumber(2, 3.1) * ComplexNumber(3, 0) == ComplexNumber(6, 9.3)


def test39():
    assert ComplexNumber(0, 3.1) * ComplexNumber(3, 1.2) == ComplexNumber(-3.72, 9.3)


def test40():
    assert ComplexNumber(2, 0) * ComplexNumber(3, 1.2) == ComplexNumber(6, 2.4)


def test41():
    assert ComplexNumber(2, 3) / ComplexNumber(3, 2) == ComplexNumber(12/13, 5/13)


def test42():
    assert ComplexNumber(0, 3) / ComplexNumber(3, 2) == ComplexNumber(6/13, 9/13)


def test43():
    assert ComplexNumber(2, 0) / ComplexNumber(3, 2) == ComplexNumber(6/13, -4/13)


def test44():
    assert ComplexNumber(2, 3) / ComplexNumber(0, 2) == ComplexNumber(3/2, -1)


def test45():
    assert ComplexNumber(2, 3) / ComplexNumber(3, 0) == ComplexNumber(2/3, 1)


def test46():
    with pytest.raises(ZeroDivisionError):
        ComplexNumber(2, 94.2) / ComplexNumber(0, 0)


def test47():
    assert ComplexNumber(0, 0) / ComplexNumber(3, 2) == ComplexNumber(0, 0)


def test48():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(2, 94.2) % ComplexNumber(0, 0)


def test49():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(2, 94.2) ^ ComplexNumber(0, 0)


M1 = Matrix(2, 2, [[Number(1.2), Number(2)], [Number(3), Number(4)]])
rowM = Matrix(1, 3, [[Number(1), Number(2), Number(3)]])
colM = Matrix(3, 1, [[Number(1)], [Number(2)], [Number(3)]])

def test50():
    assert M1 + Number(2) == Matrix(2, 2, [[Number(3.2), Number(4)], [Number(5), Number(6)]])


def test51():
    assert M1 - Number(2) == Matrix(2, 2, [[Number(-0.8), Number(0)], [Number(1), Number(2)]])


def test52():
    assert M1 * Number(2) == Matrix(2, 2, [[Number(2.4), Number(4)], [Number(6), Number(8)]])


def test53():
    assert M1 / Number(2) == Matrix(2, 2, [[Number(0.6), Number(1)], [Number(1.5), Number(2)]])


def test54():
    with pytest.raises(OperationIsNotSupported):
        Number(2) + M1


def test55():
    with pytest.raises(OperationIsNotSupported):
        Number(2) - M1


def test56():
    with pytest.raises(OperationIsNotSupported):
        Number(2) * M1


def test57():
    with pytest.raises(OperationIsNotSupported):
        Number(2) / M1


def test58():
    with pytest.raises(OperationIsNotSupported):
        Number(2) % M1


def test59():
    with pytest.raises(OperationIsNotSupported):
        Number(2) ^ M1


def test60():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(2, 7) + M1


def test61():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(2, 7) - M1


def test62():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(2, 7) * M1


def test63():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(2, 8) / M1


def test64():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(2, 8) % M1


def test65():
    with pytest.raises(OperationIsNotSupported):
        ComplexNumber(2, 1) ^ M1


def test66():
    with pytest.raises(OperationIsNotSupported):
        M1 * ComplexNumber


def test67():
    with pytest.raises(OperationIsNotSupported):
        M1 / ComplexNumber(2, 4)


def test68():
    with pytest.raises(OperationIsNotSupported):
        M1 % ComplexNumber(2, 4)


def test69():
    with pytest.raises(OperationIsNotSupported):
        M1 ^ ComplexNumber(2, 4)


def test70():
    assert M1 % Number(2) == Matrix(2, 2, [[Number(1.2%2), Number(0)], [Number(1), Number(0)]])


def test71():
    assert M1 ^ Number(3) == M1 ** M1 ** M1


def test72():
    with pytest.raises(OperationIsNotSupported):
        M1 ^ Number(0)


def test73():
    with pytest.raises(OperationIsNotSupported):
        M1 ^ Number(-1)


def test74():
    assert M1 + M1 == Matrix(2, 2, [[Number(2.4), Number(4)], [Number(6), Number(8)]])


def test75():
    assert M1 - M1 == Matrix(2, 2, [[Number(0), Number(0)], [Number(0), Number(0)]])


def test76():
    assert M1 * M1 == Matrix(2, 2, [[Number(1.44), Number(4)], [Number(9), Number(16)]])


def test77():
    assert M1 / M1 == Matrix(2, 2, [[Number(1), Number(1)], [Number(1), Number(1)]])


def test78():
    with pytest.raises(WrongMatrixDimension):
        M1 + rowM


def test79():
    with pytest.raises(WrongMatrixDimension):
        rowM * colM


def test80():
    assert M1 ** M1 == Matrix(2, 2, [[Number(7), Number(10)], [Number(15), Number(22)]])


def test81():
    assert rowM ** colM == Matrix(2, 2, [[Number(7), Number(10)], [Number(15), Number(22)]])


def test82():
    with pytest.raises(OperationIsNotSupported):
        M1 ^ M1
