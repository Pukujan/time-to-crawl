from __future__ import annotations

from dataclasses import dataclass, replace

from ttc.domain.identity import new_id

KIND_DISCOVER = "DISCOVER"
KIND_REFRESH = "REFRESH"
STATE_READY = "READY"
STATE_LEASED = "LEASED"
STATE_DONE = "DONE"
STATE_CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class WorkItem:
    url: str
    kind: str
    generation: int
    due: bool = True
    state: str = STATE_READY
    lease_id: str | None = None
    evidence_id: str | None = None


class Scheduler:
    def __init__(self) -> None:
        self._items: dict[str, WorkItem] = {}

    def enqueue(self, url: str, kind: str) -> WorkItem:
        key = _key(url, kind)
        existing = self._items.get(key)
        if existing is None:
            item = WorkItem(url=url, kind=kind, generation=1, due=True)
            self._items[key] = item
            return item
        if kind == KIND_REFRESH:
            item = replace(existing, due=True, state=STATE_READY, lease_id=None)
            self._items[key] = item
            return item
        return existing

    def claim(self, url: str, kind: str) -> WorkItem:
        key = _key(url, kind)
        item = self._items[key]
        if item.state == STATE_CANCELLED:
            raise PermissionError("cancelled")
        if not item.due and kind == KIND_REFRESH:
            raise PermissionError("not_due")
        leased = replace(
            item,
            state=STATE_LEASED,
            lease_id=new_id("lease"),
            generation=item.generation + (1 if item.state != STATE_LEASED else 0),
        )
        self._items[key] = leased
        return leased

    def complete(self, item: WorkItem, evidence_id: str) -> WorkItem:
        current = self._items[_key(item.url, item.kind)]
        if current.lease_id != item.lease_id or current.generation != item.generation:
            raise PermissionError("stale_lease")
        if current.state != STATE_LEASED:
            raise PermissionError("not_leased")
        if not evidence_id:
            raise PermissionError("evidence_required")
        done = replace(current, state=STATE_DONE, due=False, evidence_id=evidence_id)
        self._items[_key(item.url, item.kind)] = done
        return done

    def cancel(self, url: str, kind: str) -> WorkItem:
        key = _key(url, kind)
        current = self._items[key]
        cancelled = replace(
            current,
            state=STATE_CANCELLED,
            lease_id=None,
            generation=current.generation + 1,
        )
        self._items[key] = cancelled
        return cancelled

    def due_refresh(self, url: str) -> WorkItem:
        return self.enqueue(url, KIND_REFRESH)

    def get(self, url: str, kind: str) -> WorkItem:
        return self._items[_key(url, kind)]


def engine_seen_cannot_suppress_refresh(engine_seen: set[str], url: str, scheduler: Scheduler) -> WorkItem:
    engine_seen.add(url)
    return scheduler.due_refresh(url)


def _key(url: str, kind: str) -> str:
    return f"{kind}:{url}"
