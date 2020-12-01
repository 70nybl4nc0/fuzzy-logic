from .funtions import Ploteable


class FuzzySet(Ploteable):
    def __init__(self, name: str, linguistic_variable: str, membership_function):
        self.linguistic_variable = linguistic_variable
        self.name = name
        self.membership_function = membership_function

    def __call__(self, *args, **values):
        try:
            return self.membership_function(values[self.linguistic_variable])
        except KeyError:
            return self.membership_function(args[0])

    def mediat(self, domain):
        maxu, maxvs = 0, []
        for v in domain:
            u = self.membership_function(v)
            if u > maxu:
                maxvs = [v]
                maxu = u
            elif u == maxu:
                maxvs.append(v)
        return sum(maxvs) / len(maxvs)

    def centroid(self, domain):
        values = list(domain)
        num, den = 0, 0
        for v in values:
            u = self.membership_function(v)
            num += u * v
            den += u
        return num / den if den else (values[0] + values[-1]) / 2

    def bisect(self, universe):
        values = list(universe)
        images = [self.membership_function(v) for v in values]
        segments = [
            (vj - vi) * (ui + uj) / 2
            for vi, vj, ui, uj in zip(values[:-1], values[1:], images[:-1], images[1:])
        ]
        l, r = 0, len(values) - 1
        while l < r:
            m = (l + r) // 2
            lsum = sum(segments[0 : m - 1])
            rsum = sum(segments[m - 1 : -1])
            l, r = (l, m) if lsum >= rsum else (m + 1, r)
        return values[l]

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Negation(self)


class And(FuzzySet):
    def __init__(self, left: FuzzySet, right: FuzzySet):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        left = self.left(*args, **kwargs)
        right = self.right(*args, **kwargs)
        return min(left, right)


class Or(FuzzySet):
    def __init__(self, left: FuzzySet, right: FuzzySet):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        left = self.left(*args, **kwargs)
        right = self.right(*args, **kwargs)
        return max(left, right)


class Negation(FuzzySet):
    def __init__(self, object: FuzzySet):
        self.object = object

    def __call__(self, *args, **kwargs):
        return 1 - self.object(*args, **kwargs)
