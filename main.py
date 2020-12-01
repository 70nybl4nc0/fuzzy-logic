from fuzzy.funtions import Gamma, Gaussiana, L, Lambda, S, Z
from fuzzy.inference import FuzzySystem, LinguisticVariable, Rule


def interval(a, b, points=10000):
    step = (b - a) / points
    return [a + i * step for i in range(points)] + [b]


class Comida:
    Rancia = "Rancia"
    Deliciosa = "Deliciosa"


comida = LinguisticVariable(
    "Comida",
    {
        Comida.Rancia: L(0, 5),
        Comida.Deliciosa: Gamma(4, 8),
    },
)

# comida.plot(interval(0, 10))


class Servicio:
    Pobre = "Pobre"
    Bueno = "Bueno"
    Excelente = "Excelente"


servicio = LinguisticVariable(
    "Servicio",
    {
        Servicio.Pobre: Z(0, 5),
        Servicio.Bueno: Gaussiana(5, 3),
        Servicio.Excelente: S(5, 10),
    },
)


# servicio.plot(interval(0, 10))


class Propina:
    Tacaña = "Tacaña"
    Promedio = "Promedio"
    Generosa = "Generosa"


propina = LinguisticVariable(
    "Propina",
    {
        Propina.Tacaña: Lambda(0, 6.25, 12.5),
        Propina.Promedio: Lambda(6.25, 12.5, 18.75),
        Propina.Generosa: Lambda(12.5, 18.75, 25),
    },
)

# propina.plot(interval(0, 25))


# R1 : Si Servicio es Pobre ∨ Comida es Rancia −→ Propina es Taca˜na
# R2 : Si Servicio es Bueno −→ Propina es Promedio
# R3 : Si Servicio es Excelente ∨ Comida es Deliciosa −→ Propina es Generosa

rule1 = Rule(
    servicio.get(Servicio.Pobre) | comida.get(Comida.Rancia),
    propina.get(Propina.Tacaña),
)

rule11 = Rule(
    servicio.get(Servicio.Pobre) & comida.get(Comida.Rancia),
    propina.get(Propina.Tacaña),
)

rule2 = Rule(servicio.get(Servicio.Bueno), propina.get(Propina.Promedio))

rule3 = Rule(
    servicio.get(Servicio.Excelente) | comida.get(Comida.Deliciosa),
    propina.get(Propina.Generosa),
)

rule1.antecedent.plot(interval(0, 10))
# rule11.antecedent.plot(interval(0, 10))


# rule2.antecedent.plot(interval(0, 10))
# rule3.antecedent.plot(interval(0, 10))


restaurantSystem = FuzzySystem(input=(comida, servicio), output=(propina,))


restaurantSystem.add_rule(rule1)
# restaurantSystem.add_rule(rule2)
# restaurantSystem.add_rule(rule3)

# HatSelector.add_rule(rule4)


(md,) = restaurantSystem.mamdani(3, 8)

md.plot(interval(0, 25))
