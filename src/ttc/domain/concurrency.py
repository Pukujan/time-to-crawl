from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SlotPool:
    limit: int
    in_use: int = 0

    def acquire(self) -> None:
        if self.in_use >= self.limit:
            raise PermissionError("concurrency_limit")
        self.in_use += 1

    def release(self) -> None:
        if self.in_use <= 0:
            raise PermissionError("concurrency_underflow")
        self.in_use -= 1
