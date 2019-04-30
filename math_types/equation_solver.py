from math import isclose
from exceptions.evaluation_exceptions import CantSolveEquation


class NoVariableSolver:
    def solve(self, equation):
        assert len(equation) == 1
        left_term = equation.get_term_of_degree(0)
        if left_term.coef == 0:
            return "Solution is all real values."
        else:
            return "No solutions."


class LinearSolver:
    def solve(self, equation):
        variable_term = equation.get_term_of_degree(1)
        constant_term = equation.get_term_of_degree(0)
        if constant_term is None:
            return "Solution: x = 0"
        solution = (-constant_term.coef)/variable_term.coef
        return "Solution: x = {}".format(solution)


class QuadraticSolver:
    def solve(self, equation):
        a = equation.get_term_of_degree(2).coef
        b = equation.get_term_of_degree(1)
        c = equation.get_term_of_degree(0)
        b = 0 if b is None else b.coef
        c = 0 if c is None else c.coef
        discriminant = b**2 - 4*a*c

        if discriminant == 0:
            solution = "Solution: x = {}".format(-b / (2*a))
        elif discriminant > 0:
            x1 = (-b + discriminant**0.5) / (2*a)
            x2 = (-b - discriminant**0.5) / (2*a)
            if x1 > x2:
                x1, x2 = x2, x1
            solution = "Solution: x1 = {}, x2 = {}".format(x1, x2)
        else:
            real = -b / 2*a
            imag = abs(discriminant)**0.5 / (2*a)
            solution = "Solution: x1 = {real} + {imag}i, x2 = {real} - {imag}i".format(real=real, imag=imag)

        if discriminant == 0:
            discriminant_str = "zero"
        else:
            discriminant_str = "positive" if discriminant > 0 else "negative"
        discriminant_string = "Discriminant is {}".format(discriminant_str)
        return "{}\n{}".format(discriminant_string, solution)


class EquationSolver:
    SOLVABLE_DEGREES = (0, 1, 2)
    SOLVERS = {0: NoVariableSolver,
               1: LinearSolver,
               2: QuadraticSolver}

    def solve(self, equation_body):
        self.check_if_equation_solvable(equation_body)

        eq_degree = max(equation_body.degrees)
        solver = self.SOLVERS[round(eq_degree)]()
        solution_string = solver.solve(equation_body)
        return solution_string

    def check_if_equation_solvable(self, equation):
        for degree in equation.degrees:
            if not any(isclose(degree, solvable_degree) for solvable_degree in self.SOLVABLE_DEGREES):
                raise CantSolveEquation(degree)
