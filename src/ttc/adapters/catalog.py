from __future__ import annotations

from ttc.domain.models import TypedRecord


class HistoryCatalog:
    def __init__(self) -> None:
        self._current: dict[str, list[TypedRecord]] = {}
        self._history: dict[str, list[TypedRecord]] = {}

    def persist(self, records: tuple[TypedRecord, ...]) -> None:
        for record in records:
            self._history.setdefault(record.identity_key, []).append(record)
            bucket = self._current.setdefault(record.profile_id, [])
            replaced = False
            for index, existing in enumerate(bucket):
                if existing.identity_key == record.identity_key:
                    bucket[index] = record
                    replaced = True
                    break
            if not replaced:
                bucket.append(record)

    def list_by_profile(self, profile_id: str) -> tuple[TypedRecord, ...]:
        return tuple(self._current.get(profile_id, ()))

    def history_for(self, identity_key: str) -> tuple[TypedRecord, ...]:
        return tuple(self._history.get(identity_key, ()))
