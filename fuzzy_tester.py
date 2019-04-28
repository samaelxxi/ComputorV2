import math
import random
from interpreter import Interpreter
import numpy as np
from exceptions import MathException, ParsingError, EvalException, TokenizationError


E = math.e

tokens = "+-*/%^()=?[],;"
arithm_tokens = "+-*/%^"


def generate_number():
    numb = []
    i = 0
    if random.random() > 0.5:
        numb.append("-")
    while True:
        prob = random.random()
        if prob > E ** (-i / 4):
            break
        numb.append(random.choice("0123456789"))
        i += 1
    if random.random() > 0.5:
        numb.append(".")
        i = 0
        while True:
            prob = random.random()
            if prob > E ** (-i / 4):
                break
            numb.append(random.choice("0123456789"))
            i += 1
    return "".join(numb)


def generate_complex_number():
    numb = []
    real = generate_number()
    imag = generate_number()
    numb = "{} {} {}i".format(real, "-" if imag[0] == '-' else '+', imag[1:] if imag[0] == '-' else imag)
    return numb


def sample_geom_dist(p=0.5, max_k=6):
    k = np.random.geometric(p)
    if k > max_k:
        return sample_geom_dist(p, max_k)
    return k


def generate_matrix():
    rows, cols = sample_geom_dist(), sample_geom_dist()
    matrix = [[None for i in range(cols)] for j in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if random.random() > 0.3:
                el = generate_number()
            else:
                el = generate_complex_number()
            matrix[i][j] = el
    rows = ["[" + ", ".join(row) + "]" for row in matrix]
    m = "[" + "; ".join(rows) + "]"
    return m


def generate_random_token():
    if random.random() > 0.5:
        return random.choice(tokens)


def generate_math_operand():
    p = random.random()
    if p > 0.3:
        return generate_number()
    if p > 0.05:
        return generate_complex_number()
    else:
        return generate_matrix()


def generate_math_expression():
    operators = sample_geom_dist(p=0.2, max_k=10)
    expr = []
    brackets = 0
    for idx in range(operators):
        opening_bracket = False
        if random.random() > 0.7:
            brackets += 1
            opening_bracket = True
        if idx != 0:
            expr.append(random.choice(arithm_tokens))
        operand1 = generate_math_operand()
        operator = random.choice(arithm_tokens)
        operand2 = generate_math_operand()
        closing_bracket = False
        if (opening_bracket or brackets > 0) and random.random() > 0.7:
            closing_bracket = True

        if opening_bracket:
            expr.append("(")
        expr.extend([operand1, operator, operand2])
        if closing_bracket:
            expr.append(")")
            brackets -= 1
    for cl_bracket in range(brackets):
        expr.append(")")
    return " ".join(expr)


def generate_input_string():
    return generate_math_expression()


if __name__ == "__main__":
    intepr = Interpreter()
    i = 0
    while i < 1000:
        try:
            input_string = generate_input_string()
            if not input_string: continue
            print(input_string)
            output_string = intepr.eval_string(input_string)
            print(output_string)
        except (ParsingError, EvalException, MathException, TokenizationError, OverflowError, ZeroDivisionError) as e:
            print("ERROR: ", str(e))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        i += 1