from __future__ import annotations

from dataclasses import dataclass

from ttc.domain.scheduler import Scheduler


@dataclass(frozen=True)
class Health:
    status: str
    scheduler_items: int
    evidence_ok: bool
    policy_ok: bool


def probe(*, scheduler: Scheduler, evidence_ok: bool, policy_ok: bool) -> Health:
    status = "ok" if evidence_ok and policy_ok else "degraded"
    return Health(
        status=status,
        scheduler_items=len(scheduler._items),
        evidence_ok=evidence_ok,
        policy_ok=policy_ok,
    )
