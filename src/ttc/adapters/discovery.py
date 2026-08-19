from __future__ import annotations

from ttc.domain.netpolicy import classify_url
from ttc.ports.discovery import DiscoveryProviderPort


class FixtureDiscovery:
    def __init__(self, results: dict[str, tuple[str, ...]]) -> None:
        self._results = results

    def discover(self, query: str, *, profile_id: str) -> tuple[str, ...]:
        found = self._results.get(query, ())
        return tuple(url for url in found if classify_url(url) == "public")


def as_port(provider: FixtureDiscovery) -> DiscoveryProviderPort:
    return provider
