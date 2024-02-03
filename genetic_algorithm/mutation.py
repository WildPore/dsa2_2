from .individual import Individual
import random


class Mutation:
    def __init__(self, chance: float) -> None:
        self.chance = chance

    def mutate(self, individual: Individual) -> Individual:
        if random.random() < self.chance:
            return self.swap(individual)
        return individual

    def swap(self, individual: Individual) -> Individual:
        i = random.randint(1, len(individual) - 1)
        j = random.randint(1, len(individual) - 1)

        tmp = individual[i]
        individual[i] = individual[j]
        individual[j] = tmp

        return individual
