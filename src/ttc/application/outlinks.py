from __future__ import annotations

from ttc.domain.netpolicy import classify_url
from ttc.domain.scheduler import KIND_DISCOVER, Scheduler
from ttc.ports.policy import PolicyDecisionPort


def enqueue_authorized_outlinks(
    scheduler: Scheduler,
    outlinks: tuple[str, ...],
    *,
    policy: PolicyDecisionPort,
    profile_id: str,
    limit: int = 32,
) -> tuple[str, ...]:
    accepted: list[str] = []
    for url in outlinks:
        if len(accepted) >= limit:
            break
        if classify_url(url) != "public":
            continue
        decision = policy.authorize(url, profile_id=profile_id)
        if not decision.allowed:
            continue
        scheduler.enqueue(decision.url, KIND_DISCOVER)
        accepted.append(decision.url)
    return tuple(accepted)
