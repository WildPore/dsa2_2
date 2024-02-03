import random
from typing import Any
from .individual import Individual


class Chromosome:
    def __init__(
        self,
        alphabet: list,
        inclusion: list | None = None,
    ) -> None:
        self.alphabet = alphabet
        self.inclusion = inclusion

    def generate_individual(
        self, length: int, first_gene: Any | None = None, last_gene: Any | None = None
    ) -> Individual:
        """
        Generates an individual with a specified chromosome.

        Args:
            length (int): The length of the individual.
            first_gene (Any | None, optional): Inclusively sets the first gene of the chromosome, will not change length. Defaults to None.
            last_gene (Any | None, optional): Inclusively sets the last gene of the chromosome, will not change length. Defaults to None.

        Returns:
            list: An individual with the specified chromosome of required length.

        Raises:
            ValueError: If it's impossible to generate a string with required characters.
        """
        if self.inclusion is not None and len(self.inclusion) > length:
            raise ValueError(
                "The number of required characters is greater than the possible length of an individual."
            )

        permutation = [None] * length

        if first_gene is not None:
            permutation[0] = first_gene

        if last_gene is not None:
            permutation[-1] = last_gene

        # TODO This is a messy way of accomplishing the desired behavior.
        # There are also some additional considerations, like do we want
        # to provide an extension alphabet. (extension: list, additional
        # letters for the alphabet for the generation of this individual.)

        if self.inclusion is not None:
            remaining = set(self.inclusion)
        else:
            remaining = set()
        # augmented_alphabet = set(self.alphabet).update(set(self.inclusion))

        while None in permutation:
            i = random.choice(range(length))
            if permutation[i] is not None:
                continue
            if 0 < len(remaining):
                choice = random.choice(list(remaining))
                permutation[i] = choice
                remaining.remove(permutation[i])
            else:
                choice = random.choice(self.alphabet)
                permutation[i] = choice

        return Individual(permutation)
