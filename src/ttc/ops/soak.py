from __future__ import annotations

from ttc.domain.scheduler import KIND_REFRESH, STATE_DONE, Scheduler, engine_seen_cannot_suppress_refresh


def soak_refresh_cycles(url: str, cycles: int = 24, *, interval: int = 1) -> tuple[int, int]:
    scheduler = Scheduler()
    now = 0
    seen: set[str] = set()
    completed = 0
    for _ in range(cycles):
        engine_seen_cannot_suppress_refresh(seen, url, scheduler)
        claimed = scheduler.claim(url, KIND_REFRESH, now=now)
        scheduler.complete(claimed, f"ev_{completed}", now=now)
        completed += 1
        now += interval
    final = scheduler.get(url, KIND_REFRESH)
    assert final.state == STATE_DONE
    return completed, len(seen)
