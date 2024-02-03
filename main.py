from city import City
from packages import Packages
from truck import Truck
from genetic_algorithm import Chromosome, Constraint, Selection, Mutation
import random

city = City(adj_mat_fp="distances.csv")
packages = Packages(fname="packages.csv")


m1 = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
m2 = [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]
m3 = [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33]


def get_packages(manifest):
    selected_packages = []
    for id in manifest:
        selected_packages.append(packages[id])
    return selected_packages


truck1 = Truck(1, get_packages(m1), city, 480.0)
truck2 = Truck(2, get_packages(m2), city, 620.0)
truck3 = Truck(3, get_packages(m3), city, 545.0)

t1_chm = Chromosome(truck1.get_delivery_nodes(), truck1.get_delivery_nodes())
mutation = Mutation(0)


population = []
for i in range(10000):
    indiv = t1_chm.generate_individual(10)
    population.append(indiv)


def short_enough(length):
    return Constraint(
        lambda individual: city.route_length(individual.render()) < length
    )


def in_order(truck):
    return Constraint(
        lambda individual: city.route_is_on_time(
            individual.render(), truck.packages, truck.start_time
        )
    )


def generate_population(size):
    population = []
    for _ in range(size):
        indiv = t1_chm.generate_individual(10)
        population.append(indiv)
    return population


def evaluate_population(population):
    population.sort(key=lambda individual: city.route_length(individual.render()))
    return population


def update_god_route(population, god_route):
    if len(population) > 0:
        if city.route_length(population[0].render()) < city.route_length(
            god_route.render()
        ):
            god_route = population[0]
    return god_route


def print_route_info(route):
    print(
        route.render(),
        city.route_is_on_time(route.render(), get_packages(m1)),
        city.route_length(route.render()),
    )


def optimize_truck_route(truck):
    population = generate_population(10000)
    god_route = population[0]

    generations = 100
    while 0 < generations:
        if len(population) < 1:
            population = generate_population(10000)

        route_length_25p = city.route_length(
            population[int(len(population) * 0.25)].render()
        )

        length_selection = Selection(
            population, [short_enough(route_length_25p), in_order(truck)]
        )
        next_gen = length_selection.evaluate()

        population = evaluate_population(next_gen)
        god_route = update_god_route(population, god_route)

        if len(population) > 0:
            generations -= 1
        else:
            population = generate_population(10000)

    return god_route


truck1_route = optimize_truck_route(truck1)
truck2_route = optimize_truck_route(truck2)
truck3_route = optimize_truck_route(truck3)

print(truck1_route)
print(truck2_route)
print(truck3_route)
