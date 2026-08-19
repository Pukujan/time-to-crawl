from __future__ import annotations

from ttc.application.outlinks import enqueue_authorized_outlinks
from ttc.application.skeleton import WalkingSkeleton
from ttc.domain.scheduler import KIND_DISCOVER, Scheduler
from ttc.ports.policy import PolicyDecisionPort
from ttc.ports.profiles import ProfileRegistryPort


def run_discover(
    skeleton: WalkingSkeleton,
    scheduler: Scheduler,
    url: str,
    profile_id: str,
    *,
    policy: PolicyDecisionPort | None = None,
    profiles: ProfileRegistryPort | None = None,
) -> tuple[str, tuple[str, ...]]:
    scheduler.enqueue(url, KIND_DISCOVER)
    claimed = scheduler.claim(url, KIND_DISCOVER)
    result = skeleton.run(url, profile_id)
    scheduler.complete(claimed, result.evidence_id)
    queued = result.outlinks
    if policy is not None:
        limit = 32
        if profiles is not None:
            limit = profiles.get(profile_id).max_outlinks
        queued = enqueue_authorized_outlinks(
            scheduler,
            result.outlinks,
            policy=policy,
            profile_id=profile_id,
            limit=limit,
        )
    return result.evidence_id, queued
