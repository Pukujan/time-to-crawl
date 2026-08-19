from __future__ import annotations

from ttc.domain.hosts import same_registrable_host
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
    seed_url: str | None = None,
    same_host_only: bool = False,
) -> tuple[str, ...]:
    accepted: list[str] = []
    for url in outlinks:
        if len(accepted) >= limit:
            break
        if classify_url(url) != "public":
            continue
        if same_host_only and seed_url and not same_registrable_host(seed_url, url):
            continue
        decision = policy.authorize(url, profile_id=profile_id)
        if not decision.allowed:
            continue
        scheduler.enqueue(decision.url, KIND_DISCOVER)
        accepted.append(decision.url)
    return tuple(accepted)
