from __future__ import annotations

import pytest

from ttc.adapters.memory import FileProfileRegistry, MemoryCatalog
from ttc.api.gateway import BoundedGateway
from ttc.cli import load_reference_profiles
from ttc.domain.models import TypedRecord


def _record(record_id: str) -> TypedRecord:
    return TypedRecord(
        record_id=record_id,
        profile_id="jobs",
        record_type="job",
        payload={"title": record_id},
        evidence_id="ev_1",
        identity_key=record_id,
    )


def test_gateway_clamps_list_records() -> None:
    catalog = MemoryCatalog()
    catalog.persist(tuple(_record(f"r{i}") for i in range(5)))
    gateway = BoundedGateway(catalog, FileProfileRegistry(load_reference_profiles()))
    rows = gateway.invoke("list_records", profile_id="jobs", limit=2)
    assert len(rows) == 2
    with pytest.raises(PermissionError, match="limit_too_large"):
        gateway.invoke("list_records", profile_id="jobs", limit=201)
