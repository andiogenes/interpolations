class NewtonPolynomial:
    def __init__(self):
        self.__differences_cache = {}
        self.__pivots = []
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

    def __memoize_pivot(self, pivot):
        assert isinstance(pivot, tuple)

        key = (pivot[0],)
        value = pivot[1]

        self.__differences_cache[key] = value

    def add_pivot(self, pivot):
        assert isinstance(pivot, tuple)

        self.__memoize_pivot(pivot)
        self.__pivots.append(pivot[0])

        dd = self.__divided_differences(*self.__pivots)
        self.__coefs.append(dd)

    def __call__(self, x):
        acc = 0

        for i in range(0, len(self.__coefs)):
            term = self.__coefs[i]
            for j in range(0, i):
                term *= x - self.__pivots[j]

            acc += term

        return acc
