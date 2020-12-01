import math

from matplotlib import pyplot


class Ploteable:
    def plot(self, domain):
        xs = list(domain)
        ys = [self.__call__(x) for x in xs]
        pyplot.figure()
        pyplot.xlabel("x")
        pyplot.ylabel("y")
        pyplot.plot(xs, ys, "b", label=self.__class__.__name__)
        pyplot.legend()
        pyplot.show()

    def __call__(self, value):
        return 0


class Pi(Ploteable):
    def __init__(self, a, b, c, d):
        assert a <= b <= c <= d, f"Vales {a}, {b}, {c} and {d} must me in order."
        self.a, self.b, self.c, self.d = a, b, c, d

    def __call__(self, value):
        if value <= self.a:
            return 0
        if value <= self.b:
            return (value - self.a) / (self.b - self.a)
        if value <= self.c:
            return 1
        if value <= self.d:
            return (self.d - value) / (self.d - self.c)
        return 0


class Lambda(Pi):
    def __init__(self, a, b, c):
        super().__init__(a, b, b, c)


class Gamma(Ploteable):
    def __init__(self, a, b):
        assert a <= b, f"Vales {a} and {b} must me in order."
        self.a = a
        self.b = b

    def __call__(self, value):
        if value <= self.a:
            return 0
        if value <= self.b:
            return (value - self.a) / (self.b - self.a)
        if value > self.b:
            return 1


class L(Gamma):
    def __init__(self, a, b):
        super().__init__(a, b)

    def __call__(self, value):
        return 1 - super().__call__(value)


class Gaussiana(Ploteable):
    def __init__(self, mean, varaince):
        self.mean = mean
        self.variance = varaince

    def __call__(self, value):
        return math.e ** (-((value - self.mean) ** 2) / (2 * self.variance))


class S(Ploteable):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def __call__(self, value):
        if value <= self.a:
            return 0
        if value <= (self.a + self.b) / 2:
            return 2 * ((value - self.a) / (self.b - self.a)) ** 2
        if value <= self.b:
            return 1 - 2 * ((self.b - value) / (self.b - self.a)) ** 2
        return 1


class Z(S):
    def __call__(self, value):
        return 1 - super().__call__(value)


def Min(*fs):
    return lambda *args, **kwargs: min((f(*args, **kwargs) for f in fs), default=0)


def Max(*fs):
    return lambda *args, **kwargs: max((f(*args, **kwargs) for f in fs), default=0)
