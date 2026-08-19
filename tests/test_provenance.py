from __future__ import annotations

import pytest

from ttc.domain.provenance import bind


def test_provenance_requires_evidence_and_engine_identity() -> None:
    link = bind(
        record_id="rec_1",
        evidence_id="ev_1",
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id="jobs",
        run_id="run_1",
        fetched_url="https://example.com/x",
        policy_reason="allowlisted",
    )
    assert link.activity == "extract"
    with pytest.raises(ValueError, match="evidence_required"):
        bind(
            record_id="rec_1",
            evidence_id="",
            engine_id="fake",
            engine_version="0.0.0-fake",
            profile_id="jobs",
            run_id="run_1",
            fetched_url="https://example.com/x",
            policy_reason="allowlisted",
        )
