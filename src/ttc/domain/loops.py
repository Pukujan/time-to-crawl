from __future__ import annotations

from ttc.domain.scheduler import KIND_DISCOVER, KIND_REFRESH, Scheduler


def due_kinds(scheduler: Scheduler, url: str) -> tuple[str, ...]:
    kinds: list[str] = []
    try:
        discover = scheduler.get(url, KIND_DISCOVER)
        if discover.due:
            kinds.append(KIND_DISCOVER)
    except KeyError:
        pass
    try:
        refresh = scheduler.get(url, KIND_REFRESH)
        if refresh.due:
            kinds.append(KIND_REFRESH)
    except KeyError:
        pass
    return tuple(kinds)
