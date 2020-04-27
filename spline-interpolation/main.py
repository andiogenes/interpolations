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
    ax.plot(x, [polynomial(x1) for x1 in x], label='spline')

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


def process_sensitivity(_args):
    arguments_table = []

    def transform_lines(v):
        element = v.split(sep=',')

        if len(element) > 1:
            return float(element[0]), float(element[1])
        else:
            return float(element[0])

    # Read arguments table from file
    with open(_args.source, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        arguments_table = list(map(transform_lines, lines))

    # Read function expression from input and compile it in bytecode
    func_bytecode = parser.expr(str(input('Enter the function you want to calculate: '))).compile()

    # Wrapper that evaluates bytecode with given 'x' in local environment
    def func(x):
        return eval(func_bytecode, globals(), {'x': x})

    # Generate table for given function
    points_table = [x if isinstance(x, tuple) else (x, func(x)) for x in arguments_table]

    # Set up polynomial with values from table
    polynomial = CubicSpline(points_table)

    # Plotting:

    def extract_x(x):
        return x[0] if isinstance(x, tuple) else x

    x = np.linspace(
        extract_x(min(arguments_table, key=extract_x)),
        extract_x(max(arguments_table, key=extract_x)),
        num=1000
    )

    fig, ax = plt.subplots()

    # Draw plot of y=f(x)
    ax.plot(x, [func(x1) for x1 in x], label='original function')
    # Draw plot of Newton polynomial
    ax.plot(x, [polynomial(x1) for x1 in x], label='spline')

    # Mark arguments
    for x in arguments_table:
        pos = x[0] if isinstance(x, tuple) else x
        ax.axvline(x=pos, linestyle='--', color='green')

    # Mark points where y=f(x) and p(x) are equal
    for (x, y) in points_table:
        ax.scatter(x, y, color='purple')

    ax.grid()

    plt.legend()
    plt.show()

    fig.savefig(_args.plot_dest)


def process_parametric_line(_args):
    def _x(v):
        return math.cos(v * 6) * math.cos(v)

    def _y(v):
        return math.cos(v * 6) * math.sin(v)

    original_t = np.linspace(0, math.pi * 2, num=_args.points_num)
    x = [_x(v) for v in original_t]
    y = [_y(v) for v in original_t]

    mode = _args.mode

    if mode == 0:
        # # t_i = i
        t = list(range(0, _args.points_num))
    elif mode == 1:
        # # t_i = sum delta_i
        def t_i(_i):
            acc = 0
            for i in range(0, _i):
                val = (x[i + 1] - x[i]) ** 2 + (y[i + 1] - y[i]) ** 2
                acc += math.sqrt(val)

            return acc

        t = [t_i(i) for i in range(0, _args.points_num)]
    elif mode == 2:
        # t = exp(i)
        t = list(map(lambda i: math.exp(i), range(0, _args.points_num)))
    else:
        # t = 1/(i+1)
        t = list(map(lambda i: 1 / (i + 2), range(0, _args.points_num)))

    fig, ax = plt.subplots()

    x_spline = CubicSpline(zip(t, x))
    y_spline = CubicSpline(zip(t, y))

    domain = np.linspace(min(t), max(t), num=1000)

    ax.plot([x_spline(v) for v in domain], [y_spline(v) for v in domain])
    ax.grid()

    for (x, y) in zip(x, y):
        ax.scatter(x, y, color='purple')

    plt.show()

    fig.savefig(_args.plot_dest)


def parse_command_line():
    __parser = argparse.ArgumentParser(description='')
    subparsers = __parser.add_subparsers(help='sub-command help')

    function_parser = subparsers.add_parser('function')
    function_parser.add_argument('--source', dest='source', type=str, default='values.txt')
    function_parser.add_argument('--dest', dest='dest', type=str, default='result.txt')
    function_parser.add_argument('--plot-dest', dest='plot_dest', type=str, default='plot.png')
    function_parser.add_argument('--annotate-points', dest='annotate_points', type=bool, default=False)
    function_parser.set_defaults(func=process_function)

    sensitivity_parser = subparsers.add_parser('sensitivity')
    sensitivity_parser.add_argument('--source', dest='source', type=str, default='values.txt')
    sensitivity_parser.add_argument('--plot-dest', dest='plot_dest', type=str, default='plot.png')
    sensitivity_parser.set_defaults(func=process_sensitivity)

    parametric_line_parser = subparsers.add_parser('parametric_line')
    parametric_line_parser.add_argument('--points-num', dest='points_num', type=int, default=100)
    parametric_line_parser.add_argument('--plot-dest', dest='plot_dest', type=str, default='plot.png')
    parametric_line_parser.add_argument('--mode', dest='mode', type=int, default=0)
    parametric_line_parser.set_defaults(func=process_parametric_line)

    return __parser


if __name__ == "__main__":
    _parser = parse_command_line()
    args = _parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        _parser.parse_args(['--help'])
