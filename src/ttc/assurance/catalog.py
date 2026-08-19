from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "contracts" / "properties" / "property-catalog-v1.schema.json"
CATALOG = ROOT / "contracts" / "properties" / "ttc-properties-v1.json"


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def property_ids() -> tuple[str, ...]:
    return tuple(item["property_id"] for item in load_catalog()["properties"])
