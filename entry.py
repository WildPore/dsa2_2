class Entry:
    def __init__(self, k, v) -> None:
        self.k = k
        self.v = v

    def __str__(self) -> str:
        return f"({self.v}: {self.k})"
