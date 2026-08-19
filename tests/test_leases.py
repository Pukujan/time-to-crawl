from __future__ import annotations

import pytest

from ttc.domain.leases import lease_expired
from ttc.domain.scheduler import KIND_REFRESH, Scheduler


def test_expired_lease_cannot_complete() -> None:
    scheduler = Scheduler()
    url = "https://example.com/item"
    scheduler.enqueue(url, KIND_REFRESH)
    claimed = scheduler.claim(url, KIND_REFRESH, now=10)
    assert lease_expired(claimed, now=200) is True
    assert lease_expired(claimed, now=50) is False
    with pytest.raises(PermissionError, match="lease_expired"):
        scheduler.complete(claimed, "ev_1", now=200)
