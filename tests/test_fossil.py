from __future__ import annotations

import pytest

from ttc.adapters.fossil import FossilStub


def test_fossil_stub_cannot_overwrite_evidence() -> None:
    fossil = FossilStub()
    key = fossil.record_lesson("jobs", "lesson", "ev_1")
    assert key == "jobs:ev_1"
    with pytest.raises(PermissionError, match="knowledge_cannot_overwrite_evidence"):
        fossil.record_lesson("jobs", "OVERWRITE_EVIDENCE:raw", "ev_1")
    with pytest.raises(PermissionError, match="evidence_required"):
        fossil.record_lesson("jobs", "lesson", "")
