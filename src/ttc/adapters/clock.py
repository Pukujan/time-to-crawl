from __future__ import annotations


class FrozenClock:
    def __init__(self, value: int = 0) -> None:
        self.value = value

    def now(self) -> int:
        return self.value

    def advance(self, delta: int) -> int:
        self.value += delta
        return self.value
