"""Equation class implementation"""
from math import isclose
from exceptions.evaluation_exceptions import CantDetectUnknownVariable, IncorrectTerm, \
    FunctionNotExists, EvalException
from math_types import Variable, AFunction, Number, Operator
from math_types.equation_solver import EquationSolver


class Term:
    def __init__(self, coef, variable, degree):
        self.coef = coef
        self.variable = variable if degree != 0 else None
        self.degree = degree

    def __str__(self):
        if self.variable:
            if self.coef > 0:
                coef_str = self.coef if not isclose(self.coef, 1) else ""
            else:
                coef_str = self.coef if not isclose(self.coef, -1) else "-"
            if self.degree > 1:
                return "{}{}^{}".format(coef_str, self.variable, self.degree)
            return "{}{}".format(coef_str, self.variable)
        return str(self.coef)

    __repr__ = __str__

    @staticmethod
    def construct_term_from_objs(math_objs):
        """
        Takes list of math objects and tries to construct Term
        Correct sequence of objects it's Number, Operator(*), Variable, Operator(^), Number
        Some of the objects could be optional
        I fucking hate to parse things and should learn some regex by now, but I didn't so here it goes...

        :param math_objs: list of math objects
        :return: Term
        """
        def get_coef(objs):
            idx = 0
            # read sign
            sign = "+"
            if isinstance(objs[idx], Operator):
                if objs[idx].op in "+-":
                    sign = objs[idx].op
                    idx += 1
                else:
                    raise IncorrectTerm(objs)
            # read number and possible * operator
            if idx >= len(objs) or not isinstance(objs[idx], (Number, Variable)):
                raise IncorrectTerm(objs)
            if isinstance(objs[idx], Number):
                coef = objs[idx].val
                if len(objs) == idx + 1:
                    idx = idx + 1
                else:
                    if isinstance(objs[idx + 1], Operator):
                        if objs[idx + 1].op != "*":
                            raise IncorrectTerm(objs)
                        idx = idx + 2
                        if len(objs) <= idx:
                            raise IncorrectTerm(objs)
                    else:
                        idx = idx + 1
            else:
                coef = 1
                idx = idx
            if sign == "-":
                coef *= -1
            return coef, idx

        def get_variable(objs, idx):
            if len(objs) <= idx:
                variable = None
                idx = idx
            else:
                if not isinstance(objs[idx], Variable):
                    raise IncorrectTerm(objs)
                variable = objs[idx].name
                idx = idx + 1
            return variable, idx

        def get_degree(variable, objs, idx):
            if variable is None:
                degree = 0
                idx = idx
            elif len(objs) <= idx:
                degree = 1
                idx = idx
            else:
                if not isinstance(objs[idx], Operator) or objs[idx].op != "^":
                    raise IncorrectTerm(objs)
                if len(objs) <= idx + 1:
                    raise IncorrectTerm(objs)
                if not isinstance(objs[idx + 1], Number):
                    raise IncorrectTerm(objs)
                degree = objs[idx + 1].val
                idx = idx + 2
            return degree, idx

        coef, idx = get_coef(math_objs)
        variable, idx = get_variable(math_objs, idx)
        degree, idx = get_degree(variable, math_objs, idx)
        if len(math_objs) > idx:
            raise IncorrectTerm(math_objs)
        return Term(coef, variable, degree)


class Polynomial:
    """
    Class which represents polynomial as sum of terms.
    """
    def __init__(self, math_objs, variables, functions):
        math_objs = self._expand_variables_and_functions(math_objs, variables, functions)
        self.vars = None
        self.degrees = None
        self._terms = self._transform_to_terms(math_objs)

    def __len__(self):
        return len(self._terms)

    def __str__(self):
        parts = [str(self._terms[0])]
        for term in self._terms[1:]:
            term_str = str(term)
            delim = "+"
            if term_str[0] == "-":
                term_str = term_str[1:]
                delim = "-"
            parts.append(delim)
            parts.append(term_str)
        return " ".join(parts)

    def _expand_variables_and_functions(self, math_objs, variables, functions):
        """
        Scans math objects for variables and functions. Any defined variable is replaced by it's value.
        If function is defined but it's input is not, it's replaced with function body.
        If input could be evaluated, function replaced with function value.

        :param math_objs: list of objects
        :param variables: defined variables
        :param functions: defined functions
        :return: list of math objects with expanded variables and functions
        """
        new_objs = []
        for obj in math_objs:
            if isinstance(obj, Variable):
                if obj.name in variables:
                    new_objs.append(variables[obj.name].val)
                else:
                    new_objs.append(obj)
            elif isinstance(obj, AFunction):
                if obj.name not in functions:
                    raise FunctionNotExists(obj.name)
                func = functions[obj.name]
                try:
                    eval_res = func.evaluate(obj.input, variables, functions)
                    new_objs.append(eval_res)
                except EvalException:
                    new_objs.extend(func.body.body)
            else:
                new_objs.append(obj)
        return new_objs

    def _transform_to_terms(self, math_objs):
        """
        Takes list of math object and splits them to list of Terms using operators + or - as delimiters
        If any term is incorrect exception is thrown

        :param math_objs: list of math objects
        :return: list of terms
        """
        terms = []
        prev_idx = 0
        for i, obj in enumerate(math_objs):
            if isinstance(obj, Operator) and obj.op in "+-":
                if prev_idx != i:
                    terms.append(math_objs[prev_idx:i])
                prev_idx = i
        terms.append(math_objs[prev_idx:])
        return [Term.construct_term_from_objs(math_objs) for math_objs in terms]

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, terms):
        """
        terms setter. Every time variable terms is set,
        polynomial variables and degrees are recalculated.
        :param terms: list of terms
        """
        self._terms = terms
        self.vars = {term.variable for term in self._terms if term.variable is not None}
        self.degrees = {term.degree for term in self._terms}

    def reduce(self):
        """
        Sums all terms with same variable and degree. If any resulting term has coefficient zero,
        it's removed. If all terms are removed, returns list with zero term.
        """
        diff_terms = {}
        for term in self._terms:
            key = (term.variable, term.degree) if not isclose(term.degree, 0) else (None, 0)
            if key not in diff_terms:
                diff_terms[key] = [term]
            else:
                diff_terms[key].append(term)
        new_terms = []
        for term_key in sorted(diff_terms.keys(), key=lambda x: x[1], reverse=True):
            terms = diff_terms[term_key]
            new_term = terms[0]
            for other_term in terms[1:]:
                new_term.coef += other_term.coef
            if not isclose(new_term.coef, 0):
                new_terms.append(new_term)
        if not new_terms:
            new_terms = [Term(0, None, 0)]
        self.terms = new_terms

    def get_term_of_degree(self, degree):
        """
        :param degree: int
        :return: Term or None
        """
        for term in self.terms:
            if term.degree == degree:
                return term
        return None


class Equation:
    """
    Equation representation. Takes left and right parts of equation as lists
    of math objects, defined variables and functions.
    Merges both parts using Polynomial class into equation_body.
    """
    def __init__(self, left, right, variables, functions):
        left = Polynomial(left, variables, functions)
        right = Polynomial(right, variables, functions)
        for term in right.terms:
            term.coef *= -1
            left.terms.append(term)
        self.equation_body = left
        self.equation_body.reduce()
        if len(self.equation_body.vars) > 1:
            raise CantDetectUnknownVariable()

    def solve(self):
        """
        Tries to solve self using equation solver.
        :return: string with solution
        """
        solver = EquationSolver()
        solution = solver.solve(self.equation_body)
        solution_string = "Reduced equation: {}\n{}".format(self, solution)
        return solution_string

    def __str__(self):
        return str(self.equation_body) + " = 0"
