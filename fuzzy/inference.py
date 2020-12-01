from typing import Tuple

from matplotlib import pyplot

from .funtions import Max, Min, Ploteable  # noqa: F401
from .set import FuzzySet


def Min(f, v):
    def inner(*args, **kwargs):
        return min(f(*args, **kwargs), v)

    return inner


def Mult(f, v):
    def inner(*args, **kwargs):
        return f(*args, **kwargs) * v

    return inner


class LinguisticVariable:
    def __init__(self, name: str, linguistic_values: dict):
        self.name = name
        self.linguistic_values = {}
        for name in linguistic_values:
            # print(name)
            self.add_value(name, linguistic_values[name])

    def add_value(self, name: str, membership_function: Ploteable):
        self.linguistic_values[name] = membership_function
        self.__setattr__(name, membership_function)

    def get(self, linguistic_value: str):
        return FuzzySet(
            linguistic_value, self.name, self.linguistic_values[linguistic_value]
        )

    def plot(self, domain):
        pyplot.figure()
        pyplot.xlabel("x")
        pyplot.ylabel("y")
        xs = list(domain)

        for name in self.linguistic_values:
            f = self.linguistic_values[name]
            ys = [f(x) for x in xs]
            pyplot.plot(xs, ys, label=name)
            pyplot.legend()

        pyplot.show()


class Rule:
    def __init__(self, antecedent: FuzzySet, *consequences):
        self.antecedent: FuzzySet = antecedent
        self.consequences: "Tuple[FuzzySet,...]" = consequences


class FuzzySystem:
    def __init__(self, input: list, output: list):
        self.rules: "list[Rule]" = []
        self.input_variables: "list[FuzzySet]" = list(input)
        self.output_variables: "list[FuzzySet]" = list(output)

    def add_rule(self, rule: Rule):
        self.rules.append(rule)


def interval(a, b, points=10000):
    step = (b - a) / points
    return [a + i * step for i in range(points)] + [b]


def mamdani(fuzzysystem: FuzzySystem, *values):
    vector = {
        var.name: value for var, value in zip(fuzzysystem.input_variables, values)
    }
    agregation = {var.name: [] for var in fuzzysystem.output_variables}
    for rule in fuzzysystem.rules:
        v = rule.antecedent(**vector)
        # rule.antecedent.plot(interval(0, 10))
        for c in rule.consequences:
            # print(v)
            # c.plot(interval(0, 10))
            agregation[c.linguistic_variable].append(Min(c.membership_function, v))
    # for a in agregation:
    #     fs = agregation[a]
    #     for f in fs:
    #         p = FuzzySet("Agregation", "Agregation", f)
    #         p.plot(interval(0, 10))

    return [
        FuzzySet(var.name, "Mamdani", Max(*agregation[var.name]))
        for var in fuzzysystem.output_variables
    ]


def larsen(fuzzysystem: FuzzySystem, *values):
    vector = {
        var.name: value for var, value in zip(fuzzysystem.input_variables, values)
    }
    agregation = {var.name: [] for var in fuzzysystem.output_variables}
    for rule in fuzzysystem.rules:
        v = rule.antecedent(**vector)
        for c in rule.consequences:
            agregation[c.linguistic_variable].append(Mult(c.membership_function, v))
    return [
        FuzzySet(var.name, "Larsen", Max(*agregation[var.name]))
        for var in fuzzysystem.output_variables
    ]
