from utils import tdma
import numpy as np
import matplotlib.pyplot as plt

class CubicSpline:
    def __init__(self, nodes):
        self.__nodes = sorted(nodes, key=lambda x: x[0])

        self.__a = []
        self.__b = []
        self.__c = []
        self.__d = []

        self.__calculate_coeffs()

    def __calculate_coeffs(self):
        h = []

        for i, v in enumerate(self.__nodes):
            x = v[0]
            prev_x = x if i == 0 else self.__nodes[i - 1][0]

            h.append(x - prev_x)

            self.__a.append(v[1])

        tdm_a = [0]
        tdm_b = [0]
        tdm_c = [1]
        tdm_f = [0]

        for i in range(1, len(self.__nodes) - 1):
            tdm_a.append(h[i])
            tdm_c.append(2 * (h[i] + h[i + 1]))
            tdm_b.append(h[i + 1])
            tdm_f.append(6 * ((self.__a[i + 1] - self.__a[i]) / h[i + 1] - (self.__a[i] - self.__a[i - 1]) / h[i]))

        tdm_a.append(0)
        tdm_b.append(0)
        tdm_c.append(1)
        tdm_f.append(0)

        tdm_solution = tdma(tdm_a, tdm_b, tdm_c, tdm_f)

        self.__c = tdm_solution

        self.__d.append(0)
        self.__b.append(0)

        for i in range(1, len(tdm_solution)):
            self.__d.append((tdm_solution[i] - tdm_solution[i - 1]) / h[i])
            self.__b.append(
                (h[i] / 2) * tdm_solution[i] - ((h[i] ** 2) / 6) * self.__d[i] + (self.__a[i] - self.__a[i - 1]) / h[i])

    def __call__(self, x):
        p = -1
        for i, v in enumerate(self.__nodes):
            if x <= v[0]:
                p = i
                break

        if p == -1:
            return self.__nodes[len(self.__nodes) - 1][1]

        if p == 0:
            return self.__nodes[0][1]

        diff = (x - self.__nodes[p][0])

        return self.__a[p] + self.__b[p] * diff + (self.__c[p] / 2) * (diff ** 2) + (self.__d[p] / 6) * (diff ** 3)


spline = CubicSpline([(1, 5), (4, 4), (10, 6)])
print(spline(0))

nn = np.linspace(0, 15)

plt.subplots()

plt.plot(nn, [spline(x) for x in nn])

plt.show()