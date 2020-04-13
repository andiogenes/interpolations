class NewtonPolynomial:
    def __init__(self):
        self.__differences_cache = {}
        self.__nodes = []
        self.__coefs = []

    def __divided_differences(self, *args):
        assert len(args) > 0

        arguments = tuple(sorted(args))

        if arguments in self.__differences_cache:
            return self.__differences_cache[arguments]

        diff_1 = self.__divided_differences(*arguments[1:])
        diff_2 = self.__divided_differences(*arguments[:len(arguments) - 1])

        numerator = diff_1 - diff_2
        denominator = arguments[len(arguments) - 1] - arguments[0]

        self.__differences_cache[arguments] = numerator / denominator

        return self.__differences_cache[arguments]

    def __memoize_node(self, node):
        assert isinstance(node, tuple)

        key = (node[0],)
        value = node[1]

        self.__differences_cache[key] = value

    def add_node(self, node):
        assert isinstance(node, tuple)

        self.__memoize_node(node)
        self.__nodes.append(node[0])

        dd = self.__divided_differences(*self.__nodes)
        self.__coefs.append(dd)

    def __call__(self, x):
        acc = 0

        for i in range(0, len(self.__coefs)):
            term = self.__coefs[i]
            for j in range(0, i):
                term *= x - self.__nodes[j]

            acc += term

        return acc
