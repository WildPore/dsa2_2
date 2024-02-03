from collections.abc import Sequence


class Individual(Sequence):
    def __init__(self, permutation: list) -> None:
        self.permutation = permutation

    def __iter__(self):
        for element in self.permutation:
            yield element

    def __len__(self):
        return len(self.permutation)

    def __getitem__(self, index):
        return self.permutation[index]

    def __setitem__(self, index, value):
        self.permutation[index] = value

    def __str__(self) -> str:
        return str(self.permutation)

    def render(self) -> list:
        return [0] + self.permutation + [0]
