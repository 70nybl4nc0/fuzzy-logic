from fuzzy.funtions import Gamma, Gaussiana, L, Lambda, S, Z
from fuzzy.inference import FuzzySystem, LinguisticVariable, Rule, larsen, mamdani


def interval(a, b, points=10000):
    step = (b - a) / points
    return [a + i * step for i in range(points)] + [b]


class Tamano:
    Pequena = "Pequeña"
    Mediana = "Mediana"
    Grande = "Grande"


tamano = LinguisticVariable(
    "Tamano",
    {
        Tamano.Pequena: Z(0, 8),
        Tamano.Mediana: Gaussiana(5, 4),
        Tamano.Grande: S(2, 10),
    },
)

# tamano.plot(interval(0, 10))


class Color:
    Oscura = "Oscura"
    Clara = "Clara"


color = LinguisticVariable(
    "Color",
    {
        Color.Oscura: L(2, 10),
        Color.Clara: Gamma(0, 8),
    },
)


# color.plot(interval(0, 10))


class Suavidad:
    Blanda = "Blanda"
    Dura = "Dura"


suavidad = LinguisticVariable(
    "Suavidad",
    {
        Suavidad.Blanda: Z(0, 10),
        Suavidad.Dura: S(0, 10),
    },
)

# suavidad.plot(interval(0, 10))


class Calidad:
    Mala = "Mala"
    Regular = "Regular"
    Buena = "Buena"


calidad = LinguisticVariable(
    "Calidad",
    {
        Calidad.Mala: L(1, 4),
        Calidad.Regular: Lambda(2, 5, 8),
        Calidad.Buena: Gamma(5, 9),
    },
)

# calidad.plot(interval(0, 10))

# 1. Si el Color es oscuro y la Suavidad es blanda, entonces la Calidad es Mala
# 2. Si el Tamaño es pequeño, y de Color oscuro, entonces la Calidad es Mala
# 3. Si el Tamaño es pequeño y de Suavidad Dura y de Color Blanco,
#    entonces la calidad es Regular
# 4. Si el Color es claro y el tamaño mediano, entonces la Calidad es Regular
# 5. Si la Suavidad es dura y el Color es oscuro, entonces la Calidad es Regular
# 6. Si el Tamaño[^1] es grande, el Color claro, entonces la Calidad es Buena
# 7. Si el Tamaño es mediano, la Suavidad dura y el Color claro,
#    entonces la Calidad es Buena

rule_1 = Rule(
    color.get(Color.Oscura) & suavidad.get(Suavidad.Blanda),
    calidad.get(Calidad.Mala),
)

rule_2 = Rule(
    color.get(Color.Oscura) & tamano.get(Tamano.Pequena),
    calidad.get(Calidad.Mala),
)

rule_3 = Rule(
    tamano.get(Tamano.Pequena) & suavidad.get(Suavidad.Blanda),
    calidad.get(Calidad.Mala),
)

rule_4 = Rule(
    tamano.get(Tamano.Pequena) & suavidad.get(Suavidad.Dura) & color.get(Color.Clara),
    calidad.get(Calidad.Regular),
)

rule_5 = Rule(
    color.get(Color.Clara) & tamano.get(Tamano.Mediana),
    calidad.get(Calidad.Regular),
)

rule_6 = Rule(
    color.get(Color.Oscura) & suavidad.get(Suavidad.Dura),
    calidad.get(Calidad.Regular),
)

rule_7 = Rule(
    color.get(Color.Clara) & suavidad.get(Suavidad.Dura),
    calidad.get(Calidad.Regular),
)

rule_8 = Rule(
    color.get(Color.Oscura) & tamano.get(Tamano.Grande),
    calidad.get(Calidad.Regular),
)

rule_9 = Rule(
    color.get(Color.Clara) & tamano.get(Tamano.Grande),
    calidad.get(Calidad.Buena),
)

rule_10 = Rule(
    color.get(Color.Clara) & suavidad.get(Suavidad.Dura) & tamano.get(Tamano.Mediana),
    calidad.get(Calidad.Buena),
)

# rule1.antecedent.plot(interval(0, 10))

restaurantSystem = FuzzySystem(input=(tamano, color, suavidad), output=(calidad,))


restaurantSystem.add_rule(rule_1)
restaurantSystem.add_rule(rule_2)
restaurantSystem.add_rule(rule_3)
restaurantSystem.add_rule(rule_4)
restaurantSystem.add_rule(rule_5)
restaurantSystem.add_rule(rule_6)
restaurantSystem.add_rule(rule_7)
restaurantSystem.add_rule(rule_8)
restaurantSystem.add_rule(rule_9)
restaurantSystem.add_rule(rule_10)


print("\nTest 1: Tamaño 3, Color 7, Suavidad 5")

(mamd,) = mamdani(restaurantSystem, 3, 7, 5)
(lars,) = larsen(restaurantSystem, 3, 7, 5)

print(f"Mamdani: {mamd.bisect(interval(0, 10))}")
print(f"Larsen: {lars.bisect(interval(0, 10))}")

# mamd.plot(interval(0, 10))
# lars.plot(interval(0, 10))

print("\nTest 2: Tamaño 4, Color 1, Suavidad 1")

(mamd,) = mamdani(restaurantSystem, 9, 1, 1)
(mamd,) = larsen(restaurantSystem, 9, 1, 1)

print(f"Mamdani: {mamd.bisect(interval(0, 10))}")
print(f"Larsen: {lars.bisect(interval(0, 10))}")

# mamd.plot(interval(0, 10))
# lars.plot(interval(0, 10))

print("\nTest 3: Tamaño 5, Color 1, Suavidad 10")

(mamd,) = mamdani(restaurantSystem, 5, 1, 10)
(lars,) = larsen(restaurantSystem, 5, 1, 10)

print(f"Mamdani: {mamd.bisect(interval(0, 10))}")
print(f"Larsen: {lars.bisect(interval(0, 10))}")

# mamd.plot(interval(0, 10))
# lars.plot(interval(0, 10))

print("\nTest 4: Tamaño 4, Color 4, Suavidad 5")

(mamd,) = mamdani(restaurantSystem, 4, 4, 5)
(lars,) = larsen(restaurantSystem, 4, 4, 5)

print(f"Mamdani: {mamd.bisect(interval(0, 10))}")
print(f"Larsen: {lars.bisect(interval(0, 10))}")

# mamd.plot(interval(0, 10))
# lars.plot(interval(0, 10))
