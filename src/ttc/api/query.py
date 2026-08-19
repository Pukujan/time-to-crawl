from __future__ import annotations

from ttc.domain.models import TypedRecord
from ttc.ports.catalog import OperationalCatalogPort


class CatalogQuery:
    def __init__(self, catalog: OperationalCatalogPort) -> None:
        self._catalog = catalog

    def list_records(self, profile_id: str) -> tuple[TypedRecord, ...]:
        return self._catalog.list_by_profile(profile_id)
