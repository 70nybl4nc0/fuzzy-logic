from matplotlib import pyplot

from .funtions import Max, Min, Ploteable  # noqa: F401
from .set import FuzzySet


class LinguisticVariable:
    def __init__(self, name: str, linguistic_values: dict):
        self.name = name
        self.linguistic_values = {}
        for name in linguistic_values:
            print(name)
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
        self.antecedent = antecedent
        self.consequences = consequences

    def __str__(self):
        return f"{self.antecedent} => " + ", ".join(str(c) for c in self.consequences)


class FuzzySystem:
    def __init__(self, input: list, output: list):
        self.rules = []
        self.input_variables = list(input)
        self.output_variables = list(output)

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def mamdani(self, *values):
        vector = {var.name: value for var, value in zip(self.input_variables, values)}

        agregation = {var.name: [] for var in self.output_variables}

        for rule in self.rules:
            v = rule.antecedent(**vector)
            for c in rule.consequences:
                agregation[c.linguistic_variable].append(
                    lambda *args, **kwargs: min(
                        c.membership_function(*args, **kwargs), v
                    )
                )

        return [
            FuzzySet("Mamdani", var.name, Max(*agregation[var.name]))
            for var in self.output_variables
        ]

    def larsen(self, *values):
        vector = {var.name: value for var, value in zip(self.input_variables, values)}
        agregation = {var.name: [] for var in self.output_variables}

        for rule in self.rules:
            v = rule.antecedent(**vector)
            for c in rule.consequences:
                agregation[c.linguistic_variable].append(v * c.membership_function)

        return [
            FuzzySet("Larsen", var.name, Max(*agregation[var.name]))
            for var in self.output_variables
        ]
