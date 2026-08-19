from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from ttc.adapters.memory import load_profile
from ttc.domain.identity import evidence_id_for, new_id
from ttc.domain.models import Evidence, TypedRecord

SCHEMAS = Path(__file__).resolve().parents[1] / "contracts" / "schemas"
PROFILES = Path(__file__).resolve().parents[1] / "contracts" / "profiles"


def _schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def test_profile_and_record_schemas_validate() -> None:
    products = load_profile(PROFILES / "products-and-offers.v1.json")
    jobs = load_profile(PROFILES / "jobs.v1.json")
    providers = load_profile(PROFILES / "inference-providers.v1.json")
    jsonschema.validate(products.to_record(), _schema("profile-v1.schema.json"))
    jsonschema.validate(jobs.to_record(), _schema("profile-v1.schema.json"))
    jsonschema.validate(providers.to_record(), _schema("profile-v1.schema.json"))
    digest = "a" * 64
    evidence = Evidence(
        evidence_id=evidence_id_for(digest),
        content_sha256=digest,
        fetched_url="https://fixture.example/widget",
        captured_at="2026-08-19T00:00:00Z",
        content_type="application/json",
        body=b"{}",
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id=products.profile_id,
        run_id=new_id("run"),
    )
    record = TypedRecord(
        record_id=new_id("rec"),
        profile_id=products.profile_id,
        record_type="offer",
        payload={"seller_id": "seller_alpha"},
        evidence_id=evidence.evidence_id,
        identity_key="seller_alpha|https://alpha.example/widget",
    )
    jsonschema.validate(evidence.to_record(), _schema("evidence-v1.schema.json"))
    jsonschema.validate(record.to_record(), _schema("typed-record-v1.schema.json"))


def test_executable_profile_keys_are_rejected() -> None:
    data = {
        "profile_id": "evil",
        "version": "1",
        "title": "evil",
        "output_schema": "x",
        "identity_keys": ["id"],
        "code": "print('nope')",
    }
    path = PROFILES / "_tmp_evil.json"
    try:
        path.write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(ValueError, match="executable_profile_forbidden"):
            load_profile(path)
    finally:
        if path.exists():
            path.unlink()
