import numpy as np


def tdma(a, b, c, f):
    """
    Solves system of linear equations with tridiagonal matrix.
    :param a: diagonal that lies below main diagonal
    :param b: diagonal that lies above main diagonal
    :param c: main diagonal
    :param f: free terms
    :return: solution of system
    """
    assert is_zero(a[0])
    assert is_zero(b[len(b) - 1])

    alpha = [0]
    beta = [0]
    n = len(f)
    x = [0] * n

    for i in range(n - 1):
        alpha.append(-b[i] / (a[i] * alpha[i] + c[i]))
        beta.append((f[i] - a[i] * beta[i]) / (a[i] * alpha[i] + c[i]))

    x[n - 1] = (f[n - 1] - a[n - 1] * beta[n - 1]) / (c[n - 1] + a[n - 1] * alpha[n - 1])

    for i in reversed(range(n - 1)):
        x[i] = alpha[i + 1] * x[i + 1] + beta[i + 1]

    return x


def is_zero(v):
    return abs(v) < np.finfo(float).eps


def create_parametric_line(x, y):
    def parametric_line(t):
        return x(t), y(t)

    return parametric_line
