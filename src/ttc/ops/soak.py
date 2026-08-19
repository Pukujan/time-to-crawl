from __future__ import annotations

from ttc.domain.scheduler import KIND_REFRESH, STATE_DONE, Scheduler, engine_seen_cannot_suppress_refresh


def soak_refresh_cycles(url: str, cycles: int = 24) -> tuple[int, int]:
    scheduler = Scheduler()
    seen: set[str] = set()
    completed = 0
    for _ in range(cycles):
        engine_seen_cannot_suppress_refresh(seen, url, scheduler)
        claimed = scheduler.claim(url, KIND_REFRESH)
        scheduler.complete(claimed, f"ev_{completed}")
        completed += 1
    final = scheduler.get(url, KIND_REFRESH)
    assert final.state == STATE_DONE
    return completed, len(seen)
