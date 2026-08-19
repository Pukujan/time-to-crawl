from __future__ import annotations

from ttc.ops.soak import soak_refresh_cycles


def test_simulated_24_cycle_refresh_soak() -> None:
    completed, seen = soak_refresh_cycles("https://example.com/item", cycles=24)
    assert completed == 24
    assert seen == 1


def test_simulated_72_cycle_refresh_soak() -> None:
    completed, seen = soak_refresh_cycles("https://example.com/item", cycles=72)
    assert completed == 72
    assert seen == 1
