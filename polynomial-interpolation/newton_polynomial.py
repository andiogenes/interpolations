class NewtonPolynomial:
    def __init__(self):
        self.__differences_cache = {}  # cached divided differences, dict of tuple => number
        self.__nodes = []  # Interpolation nodes, list of pairs
        self.__coefs = []  # Coefficients of L_n

    def __divided_differences(self, *args):
        """
        Calculates f(x0,x1,...,xn) = (f(x0,x1,...,xn-1) - f(x1,...,xn))/(xn - x0) and memoizes result.
        :param args: Values x0, ..., xn of f(x0, ..., xn)
        :return: Calculated n-th-order difference (n = len(args) - 1)
        """
        assert len(args) > 0

        arguments = tuple(sorted(args))  # reorder args for caching

        # retrieve result if difference is already computed
        if arguments in self.__differences_cache:
            return self.__differences_cache[arguments]

        # compute n-1-th-order differences recursively
        diff_1 = self.__divided_differences(*arguments[1:])
        diff_2 = self.__divided_differences(*arguments[:len(arguments) - 1])

        numerator = diff_1 - diff_2
        denominator = arguments[len(arguments) - 1] - arguments[0]

        # memoize f(x0, ..., xn)
        self.__differences_cache[arguments] = numerator / denominator

        return self.__differences_cache[arguments]

    def __memoize_node(self, node):
        """
        Caches interpolation node (x,y) as f(x) = y
        :param node: tuple to store in cache
        """
        assert isinstance(node, tuple)

        key = (node[0],)
        value = node[1]

        self.__differences_cache[key] = value

    def add_node(self, node):
        """
        Adds n+1-st term to polynomial.
        :param node: n+1-st interpolation node
        """
        assert isinstance(node, tuple)

        self.__memoize_node(node)
        self.__nodes.append(node[0])

        dd = self.__divided_differences(*self.__nodes)
        self.__coefs.append(dd)

    def __call__(self, x):
        """
        Calculates polynomial in point x.
        """
        acc = 0

        for i in range(0, len(self.__coefs)):
            term = self.__coefs[i]
            for j in range(0, i):
                term *= x - self.__nodes[j]

            acc += term

        return acc
