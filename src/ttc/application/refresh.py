from __future__ import annotations

from ttc.application.skeleton import WalkingSkeleton
from ttc.domain.profile_policy import refresh_interval
from ttc.domain.scheduler import KIND_REFRESH, Scheduler
from ttc.ports.profiles import ProfileRegistryPort


def run_refresh(
    skeleton: WalkingSkeleton,
    scheduler: Scheduler,
    url: str,
    profile_id: str,
    *,
    now: int,
    profiles: ProfileRegistryPort,
) -> str | None:
    profile = profiles.get(profile_id)
    due = scheduler.maybe_due_refresh(url, now=now, interval=refresh_interval(profile))
    if due is None:
        return None
    claimed = scheduler.claim(url, KIND_REFRESH)
    result = skeleton.run(url, profile_id)
    scheduler.complete(claimed, result.evidence_id, now=now)
    return result.evidence_id
