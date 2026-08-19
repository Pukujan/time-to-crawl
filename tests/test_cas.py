from __future__ import annotations

from pathlib import Path

import pytest

from ttc.adapters.cas import ContentAddressedStore
from ttc.adapters.zstd import ZstdCodec
from ttc.domain.artifacts import IdentityCodec, original_sha256
from ttc.domain.identity import evidence_id_for
from ttc.domain.models import Evidence


def test_cas_dedupes_by_original_bytes(tmp_path: Path) -> None:
    store = ContentAddressedStore(tmp_path, ZstdCodec())
    payload = b"same-bytes" * 64
    first = store.put_bytes(payload)
    second = store.put_bytes(payload)
    assert first.original_sha256 == second.original_sha256 == original_sha256(payload)
    assert store.get_bytes(first.original_sha256) == payload


def test_cas_detects_corruption(tmp_path: Path) -> None:
    store = ContentAddressedStore(tmp_path, IdentityCodec())
    payload = b"honest"
    artifact = store.put_bytes(payload)
    blob = tmp_path / artifact.original_sha256[:2] / artifact.original_sha256
    blob.write_bytes(b"tampered")
    with pytest.raises(ValueError, match="integrity_failed"):
        store.get_bytes(artifact.original_sha256)


def test_cas_rejects_mismatched_evidence_hash(tmp_path: Path) -> None:
    store = ContentAddressedStore(tmp_path, IdentityCodec())
    body = b"abc"
    evidence = Evidence(
        evidence_id=evidence_id_for("d" * 64),
        content_sha256="d" * 64,
        fetched_url="https://example.com/x",
        captured_at="2026-08-19T00:00:00Z",
        content_type="text/plain",
        body=body,
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id="jobs",
        run_id="run_1",
    )
    with pytest.raises(ValueError, match="hash_mismatch"):
        store.put_evidence(evidence)
