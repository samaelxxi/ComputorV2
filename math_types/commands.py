from math_types import *
from exceptions.evaluation_exceptions import *
import matplotlib.pyplot as plt


def plot_command(func_input, variables, functions):
    """
    Special command that plots function at defined x range
    Usage: plot(func, x_1, x_2)
    func should AFunction object, should take Number and return Number
    x_1, x_2 could be Expressions which define plot x limits

    func_input: list of objects passed to plot()
    variables: dict of defined variables
    functions: dict of defined functions
    returns: None
    """
    delimiters_idx = []

    for i, obj in enumerate(func_input):
        if isinstance(obj, Operator) and obj.op == ",":
            delimiters_idx.append(i)
    if len(delimiters_idx) != 2:
        raise WrongSpecialCommandUse("plot usage: plot(func, min_x, max_x)")
    func = func_input[:delimiters_idx[0]]
    left = func_input[delimiters_idx[0]+1:delimiters_idx[1]]
    left = Expression(left).evaluate(variables, functions)
    right = func_input[delimiters_idx[1]+1:]
    right = Expression(right).evaluate(variables, functions)

    if (len(func) != 1 or not isinstance(func[0], AFunction) or
            not isinstance(left, Number) or not isinstance(right, Number)):
        raise WrongSpecialCommandUse("plot usage: plot(func, min_x, max_x)")

    if func[0].name not in functions:
        raise FunctionNotExists(func.name)
    func = functions[func[0].name]

    x = []
    dx = (right.val - left.val) / 1000
    for i in range(1000):
        x.append(left.val + dx*i)
    y = []
    for x_i in x:
        res = func.evaluate(Expression([Number(x_i)]), variables, functions)
        if not isinstance(res, Number):
            raise WrongSpecialCommandUse("Plotted function returned not a Number")
        y.append(res.val)

    plt.figure()
    plt.ion()
    plt.plot(x, y)
    plt.axhline(color="black")
    plt.axvline(color="black")
    plt.show()
    plt.pause(0.001)
    return None


def vars_command(func_input, variables, functions):
    """
    Returns string with all defined variables

    func_input: list of objects passed to vars()
    variables: dict of defined variables
    functions: dict of defined functions
    returns: string
    """
    if len(func_input) != 0:
        raise WrongSpecialCommandUse("Unexpected argument")
    vars = []
    for var in variables.values():
        vars.append(str(var))
    return "\n".join(vars)


def funcs_command(func_input, variables, functions):
    """
    Returns string with all defined functions

    func_input: list of objects passed to funcs()
    variables: dict of defined variables
    functions: dict of defined functions
    returns: string
    """
    if len(func_input) != 0:
        raise WrongSpecialCommandUse("Unexpected argument")
    vars = []
    for var in functions.values():
        vars.append(str(var))
    return "\n".join(vars)


def linreg_command(func_input, variables, functions):
    """
    usage: linreg(X, Y) where X and Y row matrices with same shape
    X and Y define set of points on 2D euclidean plane
    This functions tries to find best-fit line using normal equations.
    Then it plots points and line.

    func_input: list of objects passed to linreg()
    variables: dict of defined variables
    functions: dict of defined functions
    returns: None
    """
    # validate
    delimiters_idx = []

    for i, obj in enumerate(func_input):
        if isinstance(obj, Operator) and obj.op == ",":
            delimiters_idx.append(i)
    if len(delimiters_idx) != 1:
        raise WrongSpecialCommandUse("linreg usage: linreg(X, Y)")
    left = func_input[:delimiters_idx[0]]
    left = Expression(left).evaluate(variables, functions)
    right = func_input[delimiters_idx[0] + 1:]
    right = Expression(right).evaluate(variables, functions)

    if (not isinstance(left, Matrix) or not left.rows == 1 or not
            isinstance(right, Matrix) or not right.rows == 1 or not
            left.cols == right.cols):
        raise WrongSpecialCommandUse("X and Y matrices both should be of (1, N) shape")

    # solve lin reg
    X = Matrix(left.cols, 2, [[Number(1), left.matrix[0][i]] for i in range(left.cols)])
    Y = right.transpose_matrix()
    theta = ((X.transpose_matrix() ** X).invert_matrix() ** X.transpose_matrix() ** Y)

    f = lambda x: theta.matrix[0][0].val + theta.matrix[1][0].val * x

    # find points and x limit
    min_x = float("inf")
    max_x = float("-inf")

    for i in range(X.rows):
        val = X.matrix[i][1].val
        if val < min_x:
            min_x = val
        if val > max_x:
            max_x = val

    x_points = [X.matrix[i][1].val for i in range(X.rows)]
    y_points = [Y.matrix[i][0].val for i in range(Y.rows)]

    # plot
    plt.figure()
    plt.ion()
    plt.plot([min_x, max_x], [f(min_x), f(max_x)], color="red")
    plt.scatter(x_points, y_points)
    plt.show()
    plt.pause(0.001)
    plt.title("f(x) = {:.3f} + {:.3f}*x".format(theta.matrix[0][0].val, theta.matrix[1][0].val))

    return None
