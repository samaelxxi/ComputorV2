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
    out_str = i.eval_string(inp_str)
    assert out_str == "6"


def test1_5():
    i = Interpreter()
    inp_str = "-6"
    out_str = i.eval_string(inp_str)
    assert out_str == "-6"


def test2():
    i = Interpreter()
    inp_str = "6.45"
    out_str = i.eval_string(inp_str)
    assert out_str == "6.45"


def test3():
    i = Interpreter()
    inp_str = "[[2.0, 3.0];   [4, 9]]"
    out_str = i.eval_string(inp_str)
    assert out_str == "[ 2.0, 3.0 ]\n[  4 ,  9  ]"


# simple operations tests
def test4():
    i = Interpreter()
    inp_str = "6 + 2"
    out_str = i.eval_string(inp_str)
    assert out_str == "8"


def test5():
    i = Interpreter()
    inp_str = "4.6 + 3.2"
    out_str = i.eval_string(inp_str)
    assert out_str == "7.8"


def test6():
    i = Interpreter()
    inp_str = "6 * 4 + 2"
    out_str = i.eval_string(inp_str)
    assert out_str == "26"


def test7():
    i = Interpreter()
    inp_str = "6 + 4*i"
    out_str = i.eval_string(inp_str)
    assert out_str == "6 + 4i"


def test8():
    i = Interpreter()
    inp_str = "6 + 4.22i"
    out_str = i.eval_string(inp_str)
    assert out_str == "6.0 + 4.22i"


def test9():
    i = Interpreter()
    inp_str = "6 + 2 * 3 + 4i - 1"
    out_str = i.eval_string(inp_str)
    assert out_str == "11 + 4i"


def test11():
    i = Interpreter()
    inp_str = "6.2 + 4^3 - 25 % 2 + 10/2.5"
    out_str = i.eval_string(inp_str)
    assert out_str == "73.2"


def test11_5():
    i = Interpreter()
    inp_str = "5 - -2 + 1"
    out_str = i.eval_string(inp_str)
    assert out_str == "8"


# brackets tests
def test10():
    i = Interpreter()
    inp_str = "(2 + 3)"
    out_str = i.eval_string(inp_str)
    assert out_str == "5"


def test12():
    i = Interpreter()
    inp_str = "(2 + 3) * 5"
    out_str = i.eval_string(inp_str)
    assert out_str == "25"


def test13():
    i = Interpreter()
    inp_str = "((5 / 2) - 7) * 3.1 + (5.7 - 2)^3 - (18/2/2*3.2 - 2*(3+   1))"
    out_str = i.eval_string(inp_str)
    assert isclose(float(out_str), float("30.303"))


# variables tests
def test14():
    i = Interpreter()
    inp_str = "varA = (2 + 3) * 5"
    out_str = i.eval_string(inp_str)
    assert out_str == "25"
    assert "vara" in i._variables
    assert i._variables["vara"].val == Number(25)


def test15():
    i = Interpreter()
    inp_str = "varA = 9"
    out_str = i.eval_string(inp_str)
    inp_str = "varb = 3 + varA"
    out_str = i.eval_string(inp_str)
    assert out_str == "12"
    assert "varb" in i._variables
    assert i._variables["varb"].val == Number(12)


def test16():
    i = Interpreter()
    inp_str = "varA = -4.3"
    out_str = i.eval_string(inp_str)
    assert out_str == "-4.3"
    assert "vara" in i._variables
    assert i._variables["vara"].val == Number(-4.3)


def test17():
    i = Interpreter()
    inp_str = "varA = 2*i + 3"
    out_str = i.eval_string(inp_str)
    assert out_str == "3 + 2i"
    assert "vara" in i._variables
    assert i._variables["vara"].val == ComplexNumber(3, 2)


def test18():
    i = Interpreter()
    inp_str = "varB = -4i - 4"
    out_str = i.eval_string(inp_str)
    assert out_str == "-4 - 4i"
    assert "varb" in i._variables
    assert i._variables["varb"].val == ComplexNumber(-4, -4)


def test19():
    i = Interpreter()
    inp_str = "x=2"
    out_str = i.eval_string(inp_str)
    assert out_str == "2"
    assert "x" in i._variables
    assert i._variables["x"].val == Number(2)

    inp_str = "y=x"
    out_str = i.eval_string(inp_str)
    assert out_str == "2"
    assert "y" in i._variables
    assert i._variables["y"].val == Number(2)

    inp_str = "y=7"
    out_str = i.eval_string(inp_str)
    assert out_str == "7"
    assert "y" in i._variables
    assert i._variables["y"].val == Number(7)

    inp_str = "y = 2 * i - 4"
    out_str = i.eval_string(inp_str)
    assert out_str == "-4 + 2i"
    assert "y" in i._variables
    assert i._variables["y"].val == ComplexNumber(-4, 2)


def test20():
    i = Interpreter()
    inp_str = "varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)"
    out_str = i.eval_string(inp_str)
    assert "vara" in i._variables
    assert i._variables["vara"].val == Number(27)

    inp_str = "varB = 2 * varA - 5 %4"
    out_str = i.eval_string(inp_str)
    assert "varb" in i._variables
    assert i._variables["varb"].val == Number(53)

    inp_str = "varC = 2 * varA - varB"
    out_str = i.eval_string(inp_str)
    assert "varc" in i._variables
    assert i._variables["varc"].val == Number(1)


def test21():
    i = Interpreter()
    inp_str = "2 = ?"
    out_str = i.eval_string(inp_str)
    assert out_str == "2"

    i.eval_string("a = 3*(4 + 1)") # 15
    i.eval_string("b = 4i - 2")    # -2 + 4i
    out_str1 = i.eval_string("a + b")
    out_str2 = i.eval_string("a + b = ?")
    out_str3 = i.eval_string("c = a + b")

    assert out_str1 == out_str2 and out_str2 == out_str3 and i._variables["c"].val == ComplexNumber(13, 4)


def test22():
    i = Interpreter()

    i.eval_string("a = [[1, 2];[3, 5.5]]")
    i.eval_string("b = 2")
    out_str1 = i.eval_string("a + b")
    out_str2 = i.eval_string("a + b = ?")
    out_str3 = i.eval_string("c = a + b")

    assert out_str1 == out_str2 and out_str2 == out_str3
    assert i._variables["c"].val == Matrix(2, 2, [[Number(3), Number(4)], [Number(5), Number(7.5)]])

# functions
def test23():
    i = Interpreter()
    inp_str = " funA(x) = 2*x^5 + 4x^2 - 5*x + 4"
    out_str = i.eval_string(inp_str)
    assert out_str == "funa(x) = 2 * x ^ 5 + 4 * x ^ 2 - 5 * x + 4"
    assert "funa" in i._functions and i._functions["funa"].input.name == "x"


def test24():
    i = Interpreter()
    out_str = i.eval_string("varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)")
    out_str = i.eval_string(" varB = 2 * varA - 5 %4")
    out_str = i.eval_string("funA(x) = varA + varB * 4 - 1 / 2 + x")
    assert out_str == "funa(x) = 27 + 53 * 4 - 1 / 2 + x"
    i.eval_string("varC = 2 * varA - varB")
    out_str = i.eval_string("varD = funA(varC)")
    assert out_str == "239.5"


def test25():
    i = Interpreter()
    i.eval_string("f(x) = 2")
    assert i.eval_string("f(4)") == i.eval_string("f(342423)") == "2"


def test26():
    i = Interpreter()
    i.eval_string("f(x) = 2")
    i.eval_string("g(x) = 3x - 1")
    i.eval_string("p = 3")
    i.eval_string("k(x) = f(x) + g(x) - p")

    assert i.eval_string("k(2)") == "4"

def test26_1():
    i = Interpreter()
    i.eval_string("f(x) = 2")
    i.eval_string("g(x) = 3x - 1")
    i.eval_string("p = 3")
    i.eval_string("k(x) = f(x+1) + g(x*2 - 3) - p")

    assert i.eval_string("k(2)") == "1"


# exceptions tests
def test27():
    i = Interpreter()
    with pytest.raises(TooManyAssignments):
        i.eval_string("f(x) = 2 = 3")

def test28():
    i = Interpreter()
    with pytest.raises(TooManyAssignments):
        i.eval_string("= f(x) = 2")

def test30():
    i = Interpreter()
    with pytest.raises(UnexpectedToken):
        i.eval_string("? x = 2+3")

def test31():
    i = Interpreter()
    with pytest.raises(UnexpectedToken):
        i.eval_string("x = 2?+3")

def test32():
    i = Interpreter()
    with pytest.raises(UnexpectedToken):
        i.eval_string("? x = 2+3")

def test33():
    i = Interpreter()
    with pytest.raises(VariableNotDefined):
        i.eval_string("x = c")

def test33_5():
    i = Interpreter()
    with pytest.raises(VariableNotDefined):
        i.eval_string("x")

def test33_6():
    i = Interpreter()
    with pytest.raises(VariableNotDefined):
        i.eval_string("x = ?")

def test34():
    i = Interpreter()
    with pytest.raises(FunctionNotExists):
        i.eval_string("x = fun(2)")

def test35():
    i = Interpreter()
    i.eval_string("y(x) = 2")
    with pytest.raises(FunctionNotExists):
        i.eval_string("x = y(fun(2))")

def test36():
    i = Interpreter()
    i.eval_string("y(x) = 2")
    with pytest.raises(FunctionNotExists):
        i.eval_string("x = fun(y(2))")

def test37():
    i = Interpreter()
    with pytest.raises(OperationIsNotSupported):
        i.eval_string("x = 2 - - - 2")

def test38():
    i = Interpreter()
    with pytest.raises(NoExpectedOperand):
        i.eval_string("x = 2 +")

def test39():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval_string("/ x = 2")

def test40():
    i = Interpreter()
    with pytest.raises(NoExpectedOperand):
        i.eval_string("5 - 2 + (4 *)")

def test41():
    i = Interpreter()
    with pytest.raises(NoExpectedOperand):
        i.eval_string("+2")

def test42():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval_string("2 = 3 + 4")

def test43():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval_string("x + 5 = 3")

def test44():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval_string("45 -2i + k = 3 + 4 - 4124")

def test45():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval_string("func(5) = 3")

def test47():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart):
        i.eval_string("func(x + 2) = 3")

def test46():
    i = Interpreter()
    with pytest.raises(Exception):
        i.eval_string("-")

def test49():
    i = Interpreter()
    with pytest.raises(FunctionNotExists):
        i.eval_string("func(5 = 3)")

def test49_1():
    i = Interpreter()
    i.eval_string("func(x) = x")
    with pytest.raises(UnexpectedToken):
        i.eval_string("func(5 = 3)")


def test50():
    i = Interpreter()
    i.eval_string("x = [[2, 3]] - [[2, 3]]")
    assert(i._variables["x"].val == Matrix(1, 2, [[Number(0), Number(0)]]))


def test51():
    i = Interpreter()
    i.eval_string("f(x) = x")
    with pytest.raises(ExpressionIsNotValid):
        i.eval_string("f(())")

def test52():
    i = Interpreter()
    i.eval_string("f(x) = x")
    assert i.eval_string("f((2 + 3) * 2)") == "10"

def test53():
    i = Interpreter()
    i.eval_string("f(x) = x + 2")
    assert i.eval_string("f((2 + 3) * 2)") == "12"
    assert i.eval_string("f(3 - i)") == "5 - 1i"
    assert i.eval_string("f([[2, 3]])") == "[ 4, 5 ]"

def test54():
    i = Interpreter()
    i.eval_string("f(x) = x + 2")
    i.eval_string("y = f(2)")
    i.eval_string("g(z) = z * y")
    assert i.eval_string("g(z) = ?") == "z * y"

def test55():
    i = Interpreter()
    with pytest.raises(ExpressionIsNotValid) as e:
        i.eval_string("[[0 1]]")

def test56():
    i = Interpreter()
    assert i.eval_string("[[0 + 1]]") == "[ 1 ]"


def test57():
    i = Interpreter()
    i.eval_string("x = 6")
    i.eval_string("f(x) = x - 5")
    assert i.eval_string("[[f(x) * (2 + 3) - x]]") == "[ -1 ]"

def test58():
    i = Interpreter()
    i.eval_string("x = 6")
    i.eval_string("y = [[x - 6, x * 30]]")
    with pytest.raises(WrongMatrixElementType) as e:
        i.eval_string("[[y + 3]]")

def test59():
    i = Interpreter()
    i.eval_string("a = [[2 - i, 3 + i]; [5i, 15]]")
    i.eval_string("b = [[-2, -i]; [i, 3]]")
    assert i.eval_string("a ** b") == "[ -5 + 5i, 8 + 1i ]\n[ 0 + 5i, 50 - 0i ]"

# equations
def test60():
    i = Interpreter()
    out_str = "Reduced equation: x - 5 = 0\nSolution: x = 5.0"
    i.eval_string("f(x) = x")
    assert i.eval_string("f(x) = 5 ?") == out_str

def test67():
    i = Interpreter()
    out_str = "Reduced equation: 2x - 10 = 0\nSolution: x = 5.0"
    assert i.eval_string("2x - 10 = x + x - 2 * x ?") == out_str

def test68():
    i = Interpreter()
    with pytest.raises(CantDetectUnknownVariable) as e:
        assert i.eval_string("x = y ?") == "4"

def test70():
    i = Interpreter()
    with pytest.raises(FunctionNotExists) as e:
        assert i.eval_string("x = f(0) ?") == "4"

def test72():
    i = Interpreter()
    out_str = "Reduced equation: -1 = 0\nNo solutions."
    assert i.eval_string("0 = 1 ?") == out_str

def test73():
    i = Interpreter()
    out_str = "Reduced equation: -1 = 0\nNo solutions."
    assert i.eval_string("x = x + 1?") == out_str

def test74():
    i = Interpreter()
    out_str = "Reduced equation: 0 = 0\nSolution is all real values."
    assert i.eval_string("0 = 0 ?") == out_str

def test74_1():
    i = Interpreter()
    out_str = "Reduced equation: 0 = 0\nSolution is all real values."
    assert i.eval_string("x^0 = 1 ?") == out_str

def test74_2():
    i = Interpreter()
    out_str = "Reduced equation: 1 = 0\nNo solutions."
    assert i.eval_string("x^0 = 0 ?") == out_str

def test74_3():
    i = Interpreter()
    out_str = "Reduced equation: -x = 0\nSolution: x = 0"
    assert i.eval_string("0 = x ?") == out_str

def test75():
    i = Interpreter()
    out_str = "Reduced equation: 0 = 0\nSolution is all real values."
    assert i.eval_string("x = x ?") == out_str

def test76():
    i = Interpreter()
    out_str = "Reduced equation: 0 = 0\nSolution is all real values."
    assert i.eval_string("x^2 + 3 * x^3 - x^3 = 2*x^3 + x^2 ?") == out_str

def test77():
    i = Interpreter()
    out_str = "Reduced equation: x = 0\nSolution: x = 0"
    assert i.eval_string("x = 0 ?") == out_str

def test78():
    i = Interpreter()
    out_str = "Reduced equation: x = 0\nSolution: x = 0"
    assert i.eval_string("x^1 + 0 = 0 ?") == out_str

def test79():
    i = Interpreter()
    out_str = "Reduced equation: x - 1 = 0\nSolution: x = 1.0"
    assert i.eval_string("x = 2 - 1 ?") == out_str

def test80():
    i = Interpreter()
    out_str = "Reduced equation: 55x + 55 = 0\nSolution: x = -1.0"
    assert i.eval_string("55x^1 = 1 - 56 ?") == out_str

def test81():
    i = Interpreter()
    out_str = "Reduced equation: x^2 = 0\nDiscriminant is zero\nSolution: x = 0.0"
    assert i.eval_string("x^2 = 0 ?") == out_str

def test82():
    i = Interpreter()
    out_str = "Reduced equation: x^2 + 2x + 1 = 0\nDiscriminant is zero\nSolution: x = -1.0"
    assert i.eval_string("x^2 + 2x + 1 = 0 ?") == out_str

def test83():
    i = Interpreter()
    out_str = "Reduced equation: x^2 - x = 0\nDiscriminant is positive\nSolution: x1 = 0.0, x2 = 1.0"
    assert i.eval_string("x^2 - x = 0 ?") == out_str

def test84():
    i = Interpreter()
    out_str = "Reduced equation: x^2 - 1 = 0\nDiscriminant is positive\nSolution: x1 = -1.0, x2 = 1.0"
    assert i.eval_string("x^2 - 1 = 0 ?") == out_str

def test85():
    i = Interpreter()
    out_str = "Reduced equation: 4x^2 + 8x - 5 = 0\nDiscriminant is positive\nSolution: x1 = -2.5, x2 = 0.5"
    assert i.eval_string("x^2 + 4x - 5 = -3x^2 - 4*x + 0 ?") == out_str

def test86():
    i = Interpreter()
    out_str = "Reduced equation: x^2 + 2x + 2 = 0\nDiscriminant is negative\nSolution: x1 = -1.0 + 1.0i, x2 = -1.0 - 1.0i"
    assert i.eval_string("x^2 + 2x +2 = 0 ?") == out_str

def test87():
    i = Interpreter()
    i.eval_string("f(x) = x+2")
    i.eval_string("y = 10")
    out1 = i.eval_string("f(x) + f(y)*x^2 - y = 0 ?")
    out2 = i.eval_string("x+2 + 12x^2 - 10 = 0 ?")
    assert out1 == out2


def test88():
    i = Interpreter()
    with pytest.raises(IncorrectTerm) as e:
        out2 = i.eval_string("x+2 + 12x^2 - 10 += 0 ?")
    with pytest.raises(IncorrectTerm) as e:
        out2 = i.eval_string("x+2 + 12x^2 - 10 *= 0 ?")

# BONUSES

def test_spec_func():
    i = Interpreter()
    assert i.eval_string("sin(0)") == "0.0"
    assert i.eval_string("sin(pi/2) ") == "1.0"
    assert i.eval_string("sin(pi) ") == "0.0"
    i.eval_string("y = 0")
    assert i.eval_string("sin(y)") == "0.0"
    i.eval_string("f(x) = sin(x) - 2")
    assert i.eval_string("f(0)") == "-2.0"


def test_spec_func_exc():
    i = Interpreter()
    with pytest.raises(SpecialFunctionWrongUsage) as e:
        i.eval_string("sin(x) = 0 ?")


def test_matrix_inversion():
    i = Interpreter()
    i.eval_string("A = [[1.0, 0.0]; [0.0, 1.0]]")
    i.eval_string("Ainv = inv(A)")
    i.eval_string("B = [[4, 3]; [3, 2]]")
    i.eval_string("Binv = inv(B)")
    assert i.eval_string("A ** inv(A)") == i.eval_string("A")
    assert i.eval_string("inv(A)") == i.eval_string("Ainv")

    i.eval_string("C = [[1, 0]; [0, 0]]")
    i.eval_string("D = [[1, 0, 3]; [0, 0, 6]]")

    with pytest.raises(MatrixIsNonInvertible) as e:
        i.eval_string("inv(C)")
    with pytest.raises(MatrixIsNonInvertible) as e:
        i.eval_string("inv(D)")

    i.eval_string("K = [[1, 2, 3]]")
    i.eval_string("C = [[1]; [2]; [3]]")
    i.eval_string("transp(K) - C")


def test_special_commands_exceptions():
    i = Interpreter()
    with pytest.raises(WrongSpecialCommandUse) as e:
        i.eval_string("vars() = ?")
    with pytest.raises(WrongSpecialCommandUse) as e:
        i.eval_string("vars() = ")
    with pytest.raises(WrongSpecialCommandUse) as e:
        i.eval_string("vars() = 2 + 3")
    with pytest.raises(WrongSpecialCommandUse) as e:
        i.eval_string("plot() = x ?")
    with pytest.raises(WrongSpecialCommandUse) as e:
        i.eval_string("2 * linreg() + 3")
    with pytest.raises(WrongSpecialCommandUse) as e:
        i.eval_string("plot(2+3)")


def test_recursive_func():
    i = Interpreter()
    with pytest.raises(FunctionIsRecursive) as e:
        i.eval_string("f(x) = f(vars())")
    with pytest.raises(FunctionIsRecursive):
        i.eval_string("f(x) = f(x)")
    with pytest.raises(FunctionIsRecursive):
        i.eval_string("g(x) = x")
        i.eval_string("f(x) = g(2 + f(x))")
    with pytest.raises(FunctionIsRecursive):
        i.eval_string("g(x) = x")
        i.eval_string("k(x) = g(x) + x")
        i.eval_string("s(x) = k(x)")
        i.eval_string("g(x) = s(x)")


def test__0():
    i = Interpreter()
    with pytest.raises(WrongAssingmentLeftPart) as e:
        i.eval_string("= 2")
        i.eval_string("= x + 3 ?")
        

def test__1():
    i = Interpreter()
    with pytest.raises(UnexpectedToken) as e:
        i.eval_string("f(z) = z * y,")


def test__2():
    i = Interpreter()
    i.eval_string("x = 2")
    i.eval_string("y = 2 * [[4, 2]]")
    i.eval_string("f(z) = z * y")
    assert i.eval_string("f(2)") == "[ 16, 8 ]"

