from __future__ import annotations

import pytest

from ttc.domain.budget import Budget, BudgetTracker


def test_budget_tracker_fails_closed() -> None:
    tracker = BudgetTracker(Budget(max_requests=2, max_bytes=100, max_depth=1, max_seconds=5))
    tracker.consume(requests=1, nbytes=40)
    tracker.consume(requests=1, nbytes=40)
    with pytest.raises(PermissionError, match="budget_requests"):
        tracker.consume(requests=1)
    with pytest.raises(PermissionError, match="budget_bytes"):
        BudgetTracker(Budget(1, 10, 1, 5)).consume(nbytes=11)
