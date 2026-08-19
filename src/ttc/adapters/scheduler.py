from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ttc.domain.scheduler import Scheduler, WorkItem


class DurableScheduler(Scheduler):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = path
        if path.exists():
            self._load()

    def enqueue(self, url: str, kind: str) -> WorkItem:
        item = super().enqueue(url, kind)
        self._save()
        return item

    def claim(self, url: str, kind: str) -> WorkItem:
        item = super().claim(url, kind)
        self._save()
        return item

    def complete(self, item: WorkItem, evidence_id: str) -> WorkItem:
        done = super().complete(item, evidence_id)
        self._save()
        return done

    def cancel(self, url: str, kind: str) -> WorkItem:
        cancelled = super().cancel(url, kind)
        self._save()
        return cancelled

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {key: asdict(item) for key, item in self._items.items()}
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _load(self) -> None:
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        self._items = {key: WorkItem(**value) for key, value in raw.items()}
