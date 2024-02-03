from typing import Callable, Sized, Protocol


class Constraint(Protocol):
    func: Callable[[Sized], bool]

    def __init__(self, func: Callable[[Sized], bool]) -> None:
        self.func = func

    def __call__(self, individual: Sized) -> bool:
        return self.func(individual)
