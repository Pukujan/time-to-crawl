from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from ttc.assurance.catalog import CATALOG, SCHEMA, load_catalog, property_ids
from ttc.assurance.holdout import run_public_interface

REQUIRED = {
    "TTC-NET-001",
    "TTC-NET-002",
    "TTC-AUTH-001",
    "TTC-AUTH-002",
    "TTC-PROV-001",
    "TTC-PROV-002",
    "TTC-ENGINE-001",
    "TTC-SCHED-001",
    "TTC-SCHED-002",
    "TTC-PROFILE-001",
    "TTC-PROFILE-002",
    "TTC-ID-001",
    "TTC-KNOW-001",
    "TTC-EVID-001",
    "TTC-DEAL-001",
}


def test_property_catalog_validates() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    catalog = load_catalog()
    jsonschema.validate(catalog, schema)
    ids = set(property_ids())
    assert REQUIRED <= ids
    assert len(ids) == len(catalog["properties"])


def test_holdout_interface_hides_cases() -> None:
    missing = run_public_interface(private_suite_present=False)
    present = run_public_interface(private_suite_present=True)
    assert missing.cases_visible_to_agent is False
    assert present.cases_visible_to_agent is False
    assert missing.aggregate == "NOT_CONFIGURED"
    assert present.aggregate == "SEALED"
    assert not Path("holdouts").exists()
