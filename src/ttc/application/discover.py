from __future__ import annotations

from ttc.application.skeleton import WalkingSkeleton
from ttc.domain.scheduler import KIND_DISCOVER, Scheduler


def run_discover(skeleton: WalkingSkeleton, scheduler: Scheduler, url: str, profile_id: str) -> tuple[str, tuple[str, ...]]:
    scheduler.enqueue(url, KIND_DISCOVER)
    claimed = scheduler.claim(url, KIND_DISCOVER)
    result = skeleton.run(url, profile_id)
    scheduler.complete(claimed, result.evidence_id)
    return result.evidence_id, result.outlinks
