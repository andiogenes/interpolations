import argparse
import parser
import math  # Required by eval in process_function
import numpy as np
import matplotlib.pyplot as plt

from newton_polynomial import NewtonPolynomial


def process_points(_args):
    points_table = []

    # Read points table from file
    with open(_args.source, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        def line_to_tuple(s):
            val = s.split(sep=',')
            return int(val[0]), int(val[1])

        points_table = list(map(line_to_tuple, lines))

    # Fill polynomial with values from the table
    polynomial = NewtonPolynomial()

    for p in points_table:
        polynomial.add_pivot(p)

    # Read point from the input:
    point = int(input('Enter the point where you want to calculate the function: '))
    value = polynomial(point)

    print('P({0})={1}'.format(point, value))

    with open(_args.dest, 'w', encoding='utf-8') as f:
        f.write(str(value))


def process_function(_args):
    arguments_table = []

    # Read arguments table from file
    with open(_args.source, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        arguments_table = list(map(int, lines))

    # Read function expression from input and compile it in bytecode
    func_bytecode = parser.expr(str(input('Enter the function you want to calculate: '))).compile()

    # Wrapper that evaluates bytecode with given 'x' in local environment
    def func(x):
        return eval(func_bytecode, globals(), {'x': x})

    # Generate table for given function
    points_table = [(x, func(x)) for x in arguments_table]

    # Write table to file
    with open(_args.dest, 'w', encoding='utf-8') as f:
        formatted_points = map(lambda v: '{0}, {1}'.format(v[0], v[1]), points_table)
        f.write('\n'.join(formatted_points))

    polynomial = NewtonPolynomial()

    # Set up polynomial with values from table
    for p in points_table:
        polynomial.add_pivot(p)

    # Plotting:

    x = np.linspace(min(arguments_table) - 5, max(arguments_table) + 5)

    fig, ax = plt.subplots()

    # Draw plot of y=f(x)
    ax.plot(x, [func(x1) for x1 in x], label='original function')
    # Draw plot of Newton polynomial
    ax.plot(x, [polynomial(x1) for x1 in x], label='polynomial')

    # Mark arguments
    for x in arguments_table:
        ax.axvline(x=x, linestyle='--', color='green')

        if _args.annotate_points:
            ax.annotate(str(x), (x + 0.5, 0))

    # Mark points where y=f(x) and p(x) are equal
    for (x, y) in points_table:
        ax.scatter(x, y, color='purple')

    ax.grid()

    plt.legend()
    plt.show()

    fig.savefig(_args.plot_dest)


def parse_command_line():
    _parser = argparse.ArgumentParser(description='')
    subparsers = _parser.add_subparsers(help='sub-command help')

    point_parser = subparsers.add_parser('point')
    point_parser.add_argument('--source', dest='source', type=str, default='input.txt')
    point_parser.add_argument('--dest', dest='dest', type=str, default='result.txt')
    point_parser.set_defaults(func=process_points)

    function_parser = subparsers.add_parser('function')
    function_parser.add_argument('--source', dest='source', type=str, default='values.txt')
    function_parser.add_argument('--dest', dest='dest', type=str, default='result.txt')
    function_parser.add_argument('--plot-dest', dest='plot_dest', type=str, default='plot.png')
    function_parser.add_argument('--annotate-points', dest='annotate_points', type=bool, default=True)
    function_parser.set_defaults(func=process_function)

    return _parser


if __name__ == "__main__":
    parser = parse_command_line()
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.parse_args(['--help'])
