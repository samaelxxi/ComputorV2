from parsing.tokenizer import Tokenizer
import pytest
from exceptions.parsing_exceptions import UnknownToken

t = Tokenizer()

def test1():
    assert t.tokenize("2") == ["2"]

def test2():
    assert t.tokenize("2+3") == ["2", "+", "3"]

def test3():
    assert t.tokenize("varA = 2") == ["vara", "=", "2"]

def test4():
    assert t.tokenize("varB = 4.242") == ["varb", "=", "4.242"]

def test5():
    assert t.tokenize("varC = -4.3") == ["varc", "=", "-", "4.3"]

def test6():
    assert t.tokenize("varA = 2*i + 3") == ["vara", "=", "2", "*", "i", "+", "3"]

def test7():
    assert t.tokenize("varB = -4i - 4") == ["varb", "=", "-", "4", "i", "-", "4"]

def test8():
    assert t.tokenize("varA = [[2,3];[4,3]]") == ["vara", "=", "[", "[", "2", ",", "3",
                                                  "]", ";", "[", "4", ",", "3", "]", "]"]

def test9():
    assert t.tokenize("varB = [[3,4]]") == ["varb", "=", "[", "[", "3", ",", "4", "]", "]"]

def test10():
    assert t.tokenize("funA(x) = 2*x^5 + 4x^2 - 5*x + 4") == ["funa", "(", "x", ")", "=", "2", "*", "x", "^", "5",
                                                              '+', "4", "x", "^", "2", "-", "5", "*", "x", "+", "4"]

def test11():
    assert t.tokenize(" funB(y) = 43 * y / (4 % 2 * y)") == ["funb", "(", "y", ")", "=", "43", "*", "y", "/", "(",
                                                             "4", "%", "2", "*", "y", ")"]

def test12():
    assert t.tokenize(" varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)") == ["vara", "=", "2", "+", "4", "*", "2", "-", "5", "%",
                                                                   "4", "+", "2", "*", "(", "4", "+", "5", ")"]

def test13():
    assert t.tokenize(" varD = funA(varC)") == ["vard", "=", "funa", "(", "varc", ")"]

def test14():
    assert t.tokenize("funA(x) = y ?") == ["funa", "(", "x", ")", "=", "y", "?"]

def test15():
    assert t.tokenize("varC =2 ** varB") == ["varc", "=", "2", "**", "varb"]

def test16():
    assert t.tokenize("varD = 2 *(2 + 4 *varC -4 /3)") == ["vard", "=", "2", "*", "(", "2", "+", "4", "*", "varc",
                                                           '-', '4', '/', '3', ')']

def test17():
    assert t.tokenize("matA = [[1.51,2];[3i,2.16];[3,4]]") == ["mata", "=", "[", "[", "1.51", ",", "2", "]", ";",
                                                              "[", "3", "i", ",", "2.16", "]", ";", "[", "3",  ",", "4", "]", "]"]

def test18():
    assert t.tokenize("funC(y) =2* y     + 4  -2 **   4+9/3") == ["func", "(", "y", ")", "=", "2", "*", "y",
                                                                  "+", "4", "-", "2",
                                                                  "**", "4", "+", "9", "/", "3"]

def test19():
    assert t.tokenize("k =?hello + (boo / % = 1.3i)) * ** * *") == ["k", '=', '?', 'hello', '+', '(', 'boo', '/', '%',
                                                                    '=', '1.3', 'i', ')', ')', '*', '**', '*', '*']

def test25():
    with pytest.raises(UnknownToken):
        t.tokenize(".")

def test26():
    with pytest.raises(UnknownToken):
        t.tokenize("hello_world = 2")
