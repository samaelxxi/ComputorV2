from parsing.parser import Parser
from math_types import *
from exceptions.parsing_exceptions import *
import pytest


p = Parser()


def test1():
    inp = ("1", "+", "2", "=", "3")
    out = (Number(1), Operator("+"), Number(2), Operator("="), Number(3))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test2():
    inp = ("1.5", "=", "i", "4", "**", "329.54")
    out = (Number(1.5), Operator("="), ComplexNumber(0, 1), Number(4), Operator("**"), Number(329.54))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test3():
    inp = ("varA", "=", "[", "[", "2", ",", "3", "]", ";", "[", "4", ",", "3", "]", "]")
    out = (Variable("vara"), Operator("="), Matrix(2, 2, [[Number(2), Number(3)], [Number(4), Number(3)]]))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test4():
    inp = ("varA", "=", "2", "/", "i")
    out = (Variable("vara"), Operator("="), Number(2), Operator("/"), ComplexNumber(0, 1))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test5():
    inp = ("funA", "(", "x", ")", "=", "2", "*", "x", "^", "5", "+", "4", "x", "^", "2", "-", "5", "*", "x", "+", "4")
    out = (Function("funa", Expression([Variable("x")])), Operator("="), Number(2), Operator("*"), Variable("x"), Operator("^"), Number(5),
          Operator("+"), Number(4), Variable("x"), Operator("^"), Number(2), Operator("-"), Number(5), Operator("*"),
          Variable("x"), Operator("+"), Number(4))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test6():
    inp = ("funB", "(", "y", ")", "=", "43", "*", "y", "/", "(", "4", "%", "2", "*", "y", ")")
    out = (Function("funb", Expression([Variable("y")])), Operator("="), Number(43), Operator("*"), Variable("y"), Operator("/"),
           Operator("("), Number(4), Operator("%"), Number(2), Operator("*"), Variable("y"), Operator(")"))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test7():
    inp = ("vardddd", "=", "funchello", "(", "world", ")")
    out = (Variable("vardddd"), Operator("="), Function("funchello", Expression([Variable("world")])))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test8():
    inp = ("funA", "(", "2", ")", "+", "funB", "(", "4", ")", "=", "?")
    out = (Function("funa", Expression([Number(2)])), Operator("+"), Function("funb", Expression([Number(4)])), Operator("="), Operator("?"))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test9():
    inp = ("matrixA", "=", "[", "[", "0", "]", "]")
    out = (Variable("matrixA"), Operator("="), Matrix(1, 1, [[Number(0)]]))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test10():
    inp = ("matrixB", "?", "%", "^", "[", "[", "1", "]", ";", "[", "0", "]", ";", "[", "3", "]", "]")
    out = (Variable("matrixb"), Operator("?"), Operator("%"), Operator("^"),
           Matrix(3, 1, [[Number(1)], [Number(0)], [Number(3)]]))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test11():
    inp = ("func", "(", "x", ")", "=", "x")
    out = (Function("func", Expression([Variable("x")])), Operator("="), Variable("x"))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]

def test_func1():
    inp = ("x", "=", "func", "(", "2", "+", "3", ")")
    out = (Variable("x"), Operator("="), Function("func", Expression([Number(2), Operator("+"), Number(3)])))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]

def test11_1():
    inp = ("matrixA", "=", "[", "[", "-", "0", "]", "]")
    out = (Variable("matrixA"), Operator("="), Matrix(1, 1, [[Number(0)]]))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test11_2():
    inp = ("matrixA", "=", "[", "[", "-", "11.1", "]", "]")
    out = (Variable("matrixA"), Operator("="), Matrix(1, 1, [[Number(-11.1)]]))
    res = p.parse(inp)
    for i, elem in enumerate(res):
        assert elem == out[i]


def test12():
    inp = ("[", "]")
    with pytest.raises(EmptyMatrix) as e:
        res = p.parse(inp)


def test13():
    inp = ("[")
    with pytest.raises(NoClosingBracket) as e:
        res = p.parse(inp)


def test14():
    inp = ("[", "[", "]", "]")
    with pytest.raises(UnexpectedToken) as e:
        res = p.parse(inp)


def test15():
    inp = ("[", "0", "]")
    with pytest.raises(UnexpectedToken) as e:
        res = p.parse(inp)


def test16():
    inp = ("[", "[", "0", "1", "]", "]")
    with pytest.raises(UnexpectedToken) as e:
        res = p.parse(inp)


def test17():
    inp = ("[", "[", "0", ",", "1", "]", "[", "13.5", "]", "]")
    with pytest.raises(UnexpectedToken) as e:
        res = p.parse(inp)


def test18():
    inp = ("[", "[", "0", ",", "1", "]", ";", "[", "13.5", "]", "]")
    with pytest.raises(MatrixDiffElems) as e:
        res = p.parse(inp)


def test19():
    inp = ("[", "[", "0", ";", "1", "]", "[", "13.5", "]", "]")
    with pytest.raises(UnexpectedToken) as e:
        res = p.parse(inp)


def test20():
    inp = ("[", "[", "0", ",", "1", "]", "[", "13.5", ",", "]", "]")
    with pytest.raises(UnexpectedToken) as e:
        res = p.parse(inp)


def test21():
    inp = ("[", "[", "0", ",", "1", "]", ",", "[", "13.5", ",", "]", "]")
    with pytest.raises(UnexpectedToken) as e:
        res = p.parse(inp)

def test22():
    inp = ("fun", "(", "2", "+", "3", ")")
    res = p.parse(inp)
    assert res[0] == Function("fun", Expression([Number(2), Operator("+"), Number(3)]))

def test23():
    inp = ("x", "=", "y", "(", "fun", "(", "2", ")", ")")
    out = (Variable("x"), Operator("="), Function("y", Expression([Function("fun", Expression([Number(2)]))])))
    res = p.parse(inp)
    print(res)
    for i, elem in enumerate(res):
        assert elem == out[i]

def test24():
    inp = ("x", "=", "y", "(", "(", "2", "+", "3", ")", "*", "2", ")")
    out = (Variable("x"), Operator("="), Function("y", Expression([Operator("("), Number(2), Operator("+"),
                                                                   Number(3), Operator(")"), Operator("*"),
                                                                   Number(2)])))
    res = p.parse(inp)
    print(res)
    for i, elem in enumerate(res):
        assert elem == out[i]
