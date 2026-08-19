from __future__ import annotations

from ttc.application.skeleton import WalkingSkeleton
from ttc.domain.scheduler import KIND_REFRESH, Scheduler


def run_refresh(skeleton: WalkingSkeleton, scheduler: Scheduler, url: str, profile_id: str) -> str:
    scheduler.due_refresh(url)
    claimed = scheduler.claim(url, KIND_REFRESH)
    result = skeleton.run(url, profile_id)
    scheduler.complete(claimed, result.evidence_id)
    return result.evidence_id
