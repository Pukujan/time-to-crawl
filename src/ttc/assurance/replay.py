from __future__ import annotations

from pathlib import Path


class ReplayStore:
    def __init__(self, fixtures: dict[str, Path]) -> None:
        self._fixtures = fixtures

    def bytes_for(self, url: str) -> bytes:
        return self._fixtures[url].read_bytes()

    def urls(self) -> tuple[str, ...]:
        return tuple(self._fixtures)
