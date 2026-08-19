from __future__ import annotations

from ttc.application.outlinks import enqueue_authorized_outlinks
from ttc.application.skeleton import WalkingSkeleton
from ttc.domain.scheduler import KIND_DISCOVER, Scheduler
from ttc.ports.policy import PolicyDecisionPort


def run_discover(
    skeleton: WalkingSkeleton,
    scheduler: Scheduler,
    url: str,
    profile_id: str,
    *,
    policy: PolicyDecisionPort | None = None,
) -> tuple[str, tuple[str, ...]]:
    scheduler.enqueue(url, KIND_DISCOVER)
    claimed = scheduler.claim(url, KIND_DISCOVER)
    result = skeleton.run(url, profile_id)
    scheduler.complete(claimed, result.evidence_id)
    queued = result.outlinks
    if policy is not None:
        queued = enqueue_authorized_outlinks(
            scheduler,
            result.outlinks,
            policy=policy,
            profile_id=profile_id,
        )
    return result.evidence_id, queued
