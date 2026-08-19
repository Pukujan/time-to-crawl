from __future__ import annotations

import pytest

from ttc.adapters.graph import GraphFact, RebuildableGraph


def test_graph_projection_is_rebuildable_and_evidence_bound() -> None:
    graph = RebuildableGraph()
    fact = GraphFact(
        subject="job:REQ-1",
        predicate="posted_at",
        obj="https://example.com/item",
        evidence_id="ev_1",
        profile_id="jobs",
    )
    graph.project(fact)
    assert graph.facts() == (fact,)
    graph.wipe()
    assert graph.facts() == ()
    graph.rebuild((fact,))
    assert graph.facts() == (fact,)
    with pytest.raises(ValueError, match="evidence_required"):
        graph.project(
            GraphFact(
                subject="job:REQ-1",
                predicate="posted_at",
                obj="https://example.com/item",
                evidence_id="",
                profile_id="jobs",
            )
        )
