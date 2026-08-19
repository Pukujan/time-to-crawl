from __future__ import annotations

import pytest

from ttc.adapters.zstd import wrap_zstd
from ttc.domain.artifacts import IdentityCodec, original_sha256, wrap
from ttc.domain.models import TypedRecord


def test_identity_is_original_bytes() -> None:
    payload = b"hello-evidence"
    identity = wrap(payload, IdentityCodec())
    zstd = wrap_zstd(payload)
    assert identity.original_sha256 == original_sha256(payload)
    assert zstd.original_sha256 == identity.original_sha256
    assert zstd.codec == "zstd"
    assert zstd.body_stored != payload
    assert zstd.body_original == payload


def test_model_citation_is_not_evidence() -> None:
    with pytest.raises(TypeError):
        TypedRecord(
            record_id="rec_1",
            profile_id="jobs",
            record_type="job",
            payload={"citation": "the model said so"},
            evidence_id=None,  # type: ignore[arg-type]
            identity_key="x",
        )
