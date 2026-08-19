from __future__ import annotations

import pytest

from ttc.adapters.memory import MemoryEvidenceStore, MemoryKnowledge
from ttc.domain.identity import evidence_id_for
from ttc.domain.models import Evidence


def test_knowledge_cannot_overwrite_evidence() -> None:
    store = MemoryEvidenceStore()
    digest = "c" * 64
    evidence = Evidence(
        evidence_id=evidence_id_for(digest),
        content_sha256=digest,
        fetched_url="https://example.com/x",
        captured_at="2026-08-19T00:00:00Z",
        content_type="text/plain",
        body=b"raw-bytes",
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id="jobs",
        run_id="run_1",
    )
    store.put(evidence)
    knowledge = MemoryKnowledge(store)
    knowledge.record_lesson("jobs", "inferred fact", evidence.evidence_id)
    assert store.get(evidence.evidence_id).body == b"raw-bytes"
    with pytest.raises(KeyError):
        knowledge.record_lesson("jobs", "unbacked", "ev_missing")
