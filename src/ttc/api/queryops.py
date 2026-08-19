from __future__ import annotations

from ttc.domain.models import TypedRecord


def filter_records(
    records: tuple[TypedRecord, ...],
    *,
    field: str,
    equals: object,
) -> tuple[TypedRecord, ...]:
    return tuple(record for record in records if record.payload.get(field) == equals)


def sort_records(
    records: tuple[TypedRecord, ...],
    *,
    field: str,
    reverse: bool = False,
) -> tuple[TypedRecord, ...]:
    return tuple(sorted(records, key=lambda record: record.payload.get(field) or 0, reverse=reverse))
