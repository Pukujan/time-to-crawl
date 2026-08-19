from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GraphFact:
    subject: str
    predicate: str
    obj: str
    evidence_id: str
    profile_id: str


class RebuildableGraph:
    """Projection only. Operational evidence remains in the evidence store."""

    def __init__(self) -> None:
        self._facts: list[GraphFact] = []

    def project(self, fact: GraphFact) -> None:
        if not fact.evidence_id:
            raise ValueError("evidence_required")
        self._facts.append(fact)

    def facts(self) -> tuple[GraphFact, ...]:
        return tuple(self._facts)

    def rebuild(self, facts: tuple[GraphFact, ...]) -> None:
        self._facts = list(facts)

    def wipe(self) -> None:
        self._facts.clear()
