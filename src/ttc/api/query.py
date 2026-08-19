from __future__ import annotations

from ttc.domain.models import TypedRecord
from ttc.domain.querylimit import clamp_limit
from ttc.ports.catalog import OperationalCatalogPort


class CatalogQuery:
    def __init__(self, catalog: OperationalCatalogPort) -> None:
        self._catalog = catalog

    def list_records(self, profile_id: str, *, limit: int | None = None) -> tuple[TypedRecord, ...]:
        records = self._catalog.list_by_profile(profile_id)
        return records[: clamp_limit(limit)]
