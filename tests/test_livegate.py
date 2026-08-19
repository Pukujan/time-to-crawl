from __future__ import annotations

from ttc.domain.killswitch import is_enabled
from ttc.domain.livegate import live_engine_names, live_network_forbidden


def test_live_network_and_engines_remain_forbidden() -> None:
    assert live_network_forbidden() is True
    for engine in live_engine_names():
        assert is_enabled(engine) is False
