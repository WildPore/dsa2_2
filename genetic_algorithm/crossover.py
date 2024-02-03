import random
from .individual import Individual


def uniform_crossover(parents: list) -> list:
    child = []
    num_parents = len(parents)
    chrm_len = len(parents[0])

    for i in range(chrm_len):
        gene = parents[random.randint(0, num_parents - 1)][i]
        child.append(gene)

    # print(child)
    return Individual(child)
