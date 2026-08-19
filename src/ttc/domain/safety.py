from __future__ import annotations

from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.models import PolicyDecision
from ttc.domain.netpolicy import PolicyBroker


def default_anti_block_is_off() -> bool:
    return "anti_block" not in DEFAULT_GRANTED


def engine_config_cannot_enable_anti_block(config: dict[str, object], broker: PolicyBroker, url: str) -> PolicyDecision:
    requested = ()
    if config.get("retry_on_blocked") or config.get("anti_block"):
        requested = ("anti_block",)
    return broker.authorize(url, profile_id="jobs", requested_capabilities=requested)
