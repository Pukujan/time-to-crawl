from __future__ import annotations

import pytest

from ttc.domain.concurrency import SlotPool


def test_slot_pool_enforces_limit() -> None:
    pool = SlotPool(limit=2)
    pool.acquire()
    pool.acquire()
    with pytest.raises(PermissionError, match="concurrency_limit"):
        pool.acquire()
    pool.release()
    pool.acquire()
    pool.release()
    pool.release()
    with pytest.raises(PermissionError, match="concurrency_underflow"):
        pool.release()
