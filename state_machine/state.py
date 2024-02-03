from enum import Enum


class State(Enum):
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
