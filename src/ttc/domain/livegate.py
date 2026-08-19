from __future__ import annotations

from ttc.domain.killswitch import LIVE_ENGINES


def live_network_forbidden() -> bool:
    return True


def live_engine_names() -> frozenset[str]:
    return LIVE_ENGINES
