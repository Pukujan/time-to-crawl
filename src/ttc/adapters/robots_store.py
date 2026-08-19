from __future__ import annotations

from pathlib import Path

from ttc.domain.robots import robots_allows


class FixtureRobots:
    def __init__(self, mapping: dict[str, Path]) -> None:
        self._mapping = mapping

    def allows(self, origin: str, path: str) -> bool:
        file = self._mapping.get(origin)
        if file is None:
            return True
        return robots_allows(file.read_text(encoding="utf-8"), path)
