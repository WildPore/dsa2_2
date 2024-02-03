class Population:
    def __init__(self, chromosome, pop_size) -> None:
        self.chromosome = chromosome
        self.population = []

        for i in range(pop_size):
            self.population.append(self.chromosome.generate_individual())
