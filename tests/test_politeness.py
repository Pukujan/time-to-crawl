from __future__ import annotations

from ttc.domain.politeness import Politeness, can_fetch, next_allowed_at


def test_politeness_delay_blocks_until_window() -> None:
    idle = Politeness(min_delay_ms=1000)
    assert can_fetch(idle, now=0) is True
    paced = Politeness(min_delay_ms=1000, last_fetch_at=10)
    assert next_allowed_at(paced) == 1010
    assert can_fetch(paced, now=1009) is False
    assert can_fetch(paced, now=1010) is True
