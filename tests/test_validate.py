from __future__ import annotations

import pytest

from ttc.application.validate import validate_payload

JOB_SCHEMA = {
    "type": "object",
    "required": ["title", "requisition_id"],
    "properties": {
        "title": {"type": "string", "minLength": 1},
        "requisition_id": {"type": "string", "minLength": 1},
    },
}


def test_payload_schema_rejects_missing_required_fields() -> None:
    validate_payload({"title": "Staff", "requisition_id": "REQ-1"}, JOB_SCHEMA)
    with pytest.raises(Exception):
        validate_payload({"title": "Staff"}, JOB_SCHEMA)
