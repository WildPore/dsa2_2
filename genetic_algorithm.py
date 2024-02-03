from genetic_algorithm import Chromosome, Selection, Constraint
from city import City

city = City("distances.csv")


def route_length(maximum_length) -> Constraint:
    return Constraint(lambda individual: city.route_length(individual) < maximum_length)
