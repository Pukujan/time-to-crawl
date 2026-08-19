from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Budget:
    max_requests: int
    max_bytes: int
    max_depth: int
    max_seconds: int


class BudgetTracker:
    def __init__(self, budget: Budget) -> None:
        self.budget = budget
        self.requests = 0
        self.bytes = 0
        self.depth = 0
        self.seconds = 0

    def consume(self, *, requests: int = 0, nbytes: int = 0, depth: int = 0, seconds: int = 0) -> None:
        self.requests += requests
        self.bytes += nbytes
        self.depth = max(self.depth, depth)
        self.seconds += seconds
        if self.requests > self.budget.max_requests:
            raise PermissionError("budget_requests")
        if self.bytes > self.budget.max_bytes:
            raise PermissionError("budget_bytes")
        if self.depth > self.budget.max_depth:
            raise PermissionError("budget_depth")
        if self.seconds > self.budget.max_seconds:
            raise PermissionError("budget_time")
