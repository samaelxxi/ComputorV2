from interpreter import Interpreter
from math_types import *
import pytest
from exceptions.evaluation_exceptions import *
from exceptions.parsing_exceptions import UnexpectedToken
from exceptions.math_exceptions import OperationIsNotSupported
from math import isclose

# basic print tests
def test1():
    i = Interpreter()
    inp_str = "6"
    out_str = i.eval(inp_str)
    assert out_str == "6"


def test1_5():
    i = Interpreter()
    inp_str = "-6"
    out_str = i.eval(inp_str)
    assert out_str == "-6"


def test2():
    i = Interpreter()
    inp_str = "6.45"
    out_str = i.eval(inp_str)
    assert out_str == "6.45"


def test3():
    i = Interpreter()
    inp_str = "[[2.0, 3.0];   [4, 9]]"
    out_str = i.eval(inp_str)
    assert out_str == "[ 2.0, 3.0 ]\n[  4 ,  9  ]"


# simple operations tests
def test4():
    i = Interpreter()
    inp_str = "6 + 2"
    out_str = i.eval(inp_str)
    assert out_str == "8"


def test5():
    i = Interpreter()
    inp_str = "4.6 + 3.2"
    out_str = i.eval(inp_str)
    assert out_str == "7.8"


def test6():
    i = Interpreter()
    inp_str = "6 * 4 + 2"
    out_str = i.eval(inp_str)
    assert out_str == "26"


def test7():
    i = Interpreter()
    inp_str = "6 + 4*i"
    out_str = i.eval(inp_str)
    assert out_str == "6 + 4i"


def test8():
    i = Interpreter()
    inp_str = "6 + 4.22i"
    out_str = i.eval(inp_str)
    assert out_str == "6.0 + 4.22i"


def test9():
    i = Interpreter()
    inp_str = "6 + 2 * 3 + 4i - 1"
    out_str = i.eval(inp_str)
    assert out_str == "11 + 4i"


def test11():
    i = Interpreter()
    inp_str = "6.2 + 4^3 - 25 % 2 + 10/2.5"
    out_str = i.eval(inp_str)
    assert out_str == "73.2"


def test11_5():
    i = Interpreter()
    inp_str = "5 - -2 + 1"
    out_str = i.eval(inp_str)
    assert out_str == "8"


# brackets tests
def test10():
    i = Interpreter()
    inp_str = "(2 + 3)"
    out_str = i.eval(inp_str)
    assert out_str == "5"


def test12():
    i = Interpreter()
    inp_str = "(2 + 3) * 5"
    out_str = i.eval(inp_str)
    assert out_str == "25"


def test13():
    i = Interpreter()
    inp_str = "((5 / 2) - 7) * 3.1 + (5.7 - 2)^3 - (18/2/2*3.2 - 2*(3+   1))"
    out_str = i.eval(inp_str)
    assert isclose(float(out_str), float("30.303"))


# variables tests
def test14():
    i = Interpreter()
    inp_str = "varA = (2 + 3) * 5"
    out_str = i.eval(inp_str)
    assert out_str == "25"
    assert "vara" in i.variables
    assert i.variables["vara"].val == Number(25)


def test15():
    i = Interpreter()
    inp_str = "varA = 9"
    out_str = i.eval(inp_str)
    inp_str = "varb = 3 + varA"
    out_str = i.eval(inp_str)
    assert out_str == "12"
    assert "varb" in i.variables
    assert i.variables["varb"].val == Number(12)


def test16():
    i = Interpreter()
    inp_str = "varA = -4.3"
    out_str = i.eval(inp_str)
    assert out_str == "-4.3"
    assert "vara" in i.variables
    assert i.variables["vara"].val == Number(-4.3)


def test17():
    i = Interpreter()
    inp_str = "varA = 2*i + 3"
    out_str = i.eval(inp_str)
    assert out_str == "3 + 2i"
    assert "vara" in i.variables
    assert i.variables["vara"].val == ComplexNumber(3, 2)


def test18():
    i = Interpreter()
    inp_str = "varB = -4i - 4"
    out_str = i.eval(inp_str)
    assert out_str == "-4 - 4i"
    assert "varb" in i.variables
    assert i.variables["varb"].val == ComplexNumber(-4, -4)


def test19():
    i = Interpreter()
    inp_str = "x=2"
    out_str = i.eval(inp_str)
    assert out_str == "2"
    assert "x" in i.variables
    assert i.variables["x"].val == Number(2)

    inp_str = "y=x"
    out_str = i.eval(inp_str)
    assert out_str == "2"
    assert "y" in i.variables
    assert i.variables["y"].val == Number(2)

    inp_str = "y=7"
    out_str = i.eval(inp_str)
    assert out_str == "7"
    assert "y" in i.variables
    assert i.variables["y"].val == Number(7)

    inp_str = "y = 2 * i - 4"
    out_str = i.eval(inp_str)
    assert out_str == "-4 + 2i"
    assert "y" in i.variables
    assert i.variables["y"].val == ComplexNumber(-4, 2)


def test20():
    i = Interpreter()
    inp_str = "varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)"
    out_str = i.eval(inp_str)
    assert "vara" in i.variables
    assert i.variables["vara"].val == Number(27)

    inp_str = "varB = 2 * varA - 5 %4"
    out_str = i.eval(inp_str)
    assert "varb" in i.variables
    assert i.variables["varb"].val == Number(53)

    inp_str = "varC = 2 * varA - varB"
    out_str = i.eval(inp_str)
    assert "varc" in i.variables
    assert i.variables["varc"].val == Number(1)


def test21():
    i = Interpreter()
    inp_str = "2 = ?"
    out_str = i.eval(inp_str)
    assert out_str == "2"

    i.eval("a = 3*(4 + 1)") # 15
    i.eval("b = 4i - 2")    # -2 + 4i
    out_str1 = i.eval("a + b")
    out_str2 = i.eval("a + b = ?")
    out_str3 = i.eval("c = a + b")

    assert out_str1 == out_str2 and out_str2 == out_str3 and i.variables["c"].val == ComplexNumber(13, 4)


def test22():
    i = Interpreter()

    i.eval("a = [[1, 2];[3, 5.5]]")
    i.eval("b = 2")
    out_str1 = i.eval("a + b")
    out_str2 = i.eval("a + b = ?")
    out_str3 = i.eval("c = a + b")

    assert out_str1 == out_str2 and out_str2 == out_str3 and i.variables["c"].val == Matrix(2, 2, [[3, 4],[ 5, 7.5]])

# functions
def test23():
    i = Interpreter()
    inp_str = " funA(x) = 2*x^5 + 4x^2 - 5*x + 4"
    out_str = i.eval(inp_str)
    assert out_str == "2 * x^5 + 4 * x^2 - 5*x + 4"
    assert "funa" in i.functions and i.functions["funa"].name == "x"


def test24():
    i = Interpreter()
    out_str = i.eval("varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)")
    out_str = i.eval(" varB = 2 * varA - 5 %4")
    out_str = i.eval("funA(x) = varA + varB * 4 - 1 / 2 + x")
    assert out_str == "238.5 + x"
    i.eval("varC = 2 * varA - varB")
    out_str = i.eval("varD = funA(varC)")
    assert out_str == "239.5"


def test25():
    i = Interpreter()
    i.eval("f(x) = 2")
    assert i.eval("f(4)") == i.eval("f(342423)") == "2"


def test26():
    i = Interpreter()
    i.eval("f(x) = 2")
    i.eval("g(x) = 3x - 1")
    i.eval("p = 3")
    i.eval("k(x) = f(x) + g(x) - p")

    assert i.eval("k(2)") == "4"


# exceptions tests
def test27():
    i = Interpreter()
    with pytest.raises(TooManyAssignments):
        i.eval("f(x) = 2 = 3")

def test28():
    i = Interpreter()
    with pytest.raises(TooManyAssignments):
        i.eval("= f(x) = 2")

def test29():
    i = Interpreter()
    with pytest.raises(UnexpectedToken):
        i.eval("2 = 2 ?")

def test30():
    i = Interpreter()
    with pytest.raises(UnexpectedToken):
        i.eval("? x = 2+3")

def test31():
    i = Interpreter()
    with pytest.raises(UnexpectedToken):
        i.eval("x = 2?+3")

def test32():
    i = Interpreter()
    with pytest.raises(UnexpectedToken):
        i.eval("? x = 2+3")

def test33():
    i = Interpreter()
    with pytest.raises(VariableNotDefined):
        i.eval("x = c")

def test33_5():
    i = Interpreter()
    with pytest.raises(VariableNotDefined):
        i.eval("x")

def test33_6():
    i = Interpreter()
    with pytest.raises(VariableNotDefined):
        i.eval("x = ?")

def test34():
    i = Interpreter()
    with pytest.raises(FunctionNotExists):
        i.eval("x = fun(2)")

def test35():
    i = Interpreter()
    i.eval("y(x) = 2")
    with pytest.raises(FunctionNotExists):
        i.eval("x = y(fun(2))")

def test36():
    i = Interpreter()
    i.eval("y(x) = 2")
    with pytest.raises(FunctionNotExists):
        i.eval("x = fun(y(2))")

def test37():
    i = Interpreter()
    with pytest.raises(OperationIsNotSupported):
        i.eval("x = 2 - - - 2")

def test38():
    i = Interpreter()
    with pytest.raises(NoExpectedOperand):
        i.eval("x = 2 +")

def test39():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval("/ x = 2")

def test40():
    i = Interpreter()
    with pytest.raises(NoExpectedOperand):
        i.eval("5 - 2 + (4 *)")

def test41():
    i = Interpreter()
    with pytest.raises(NoExpectedOperand):
        i.eval("+2")

def test42():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval("2 = 3 + 4")

def test43():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval("x + 5 = 3")

def test44():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval("45 -2i + k = 3 + 4 - 4124")

def test45():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval("func(5) = 3")

def test46():
    i = Interpreter()
    with pytest.raises(Exception):
        i.eval("-")
