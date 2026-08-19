from __future__ import annotations

from ttc.domain.budget import Budget, BudgetTracker
from ttc.domain.models import CrawlResult


def consume_result(tracker: BudgetTracker, result: CrawlResult, *, depth: int = 0) -> None:
    tracker.consume(requests=1, nbytes=len(result.body), depth=depth)
