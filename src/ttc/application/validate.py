from __future__ import annotations

import jsonschema


def validate_payload(payload: dict[str, object], schema: dict) -> None:
    jsonschema.validate(payload, schema)
