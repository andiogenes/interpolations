import argparse
import parser
import math  # Required by eval in process_function
import numpy as np
import matplotlib.pyplot as plt

from cubic_spline import CubicSpline


def process_function(_args):
    arguments_table = []

    # Read arguments table from file
    with open(_args.source, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        arguments_table = list(map(float, lines))

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

    # Set up polynomial with values from table
    polynomial = CubicSpline(points_table)

    # Plotting:

    x = np.linspace(min(arguments_table), max(arguments_table), num=1000)

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
    __parser = argparse.ArgumentParser(description='')
    subparsers = __parser.add_subparsers(help='sub-command help')

    function_parser = subparsers.add_parser('function')
    function_parser.add_argument('--source', dest='source', type=str, default='values.txt')
    function_parser.add_argument('--dest', dest='dest', type=str, default='result.txt')
    function_parser.add_argument('--plot-dest', dest='plot_dest', type=str, default='plot.png')
    function_parser.add_argument('--annotate-points', dest='annotate_points', type=bool, default=True)
    function_parser.set_defaults(func=process_function)

    return __parser


if __name__ == "__main__":
    _parser = parse_command_line()
    args = _parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        _parser.parse_args(['--help'])