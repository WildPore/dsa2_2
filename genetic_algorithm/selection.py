from . import Constraint


class Selection:
    constraints: list[Constraint]

    def __init__(self, population: list, constraints: list[Constraint]) -> None:
        self.population = population
        self.constraints = constraints

    def evaluate(self) -> list:
        selected = []
        for individual in self.population:
            if all(constraint(individual) for constraint in self.constraints):
                selected.append(individual)
        return selected

    def add_constraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)
