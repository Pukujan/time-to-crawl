from __future__ import annotations

import pytest

from ttc.domain.hostslots import HostSlotMap


def test_host_slots_are_independent() -> None:
    slots = HostSlotMap(per_host=1)
    slots.acquire("https://a.example/x")
    slots.acquire("https://b.example/x")
    with pytest.raises(PermissionError, match="concurrency_limit"):
        slots.acquire("https://a.example/y")
    slots.release("https://a.example/x")
    slots.acquire("https://a.example/y")
