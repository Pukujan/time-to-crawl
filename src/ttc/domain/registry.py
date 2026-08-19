from __future__ import annotations

from dataclasses import dataclass

from ttc.domain.netpolicy import classify_url, is_forbidden_class
from ttc.domain.urls import canonicalize


@dataclass(frozen=True)
class SourceRecord:
    url: str
    proposed_by: str
    authorized: bool
    profile_id: str


class SourceRegistry:
    def __init__(self) -> None:
        self._items: dict[str, SourceRecord] = {}

    def propose(self, url: str, *, proposed_by: str, profile_id: str) -> SourceRecord:
        canonical = canonicalize(url)
        network_class = classify_url(canonical)
        if is_forbidden_class(network_class):
            raise PermissionError(f"forbidden_network:{network_class}")
        record = SourceRecord(
            url=canonical,
            proposed_by=proposed_by,
            authorized=False,
            profile_id=profile_id,
        )
        self._items[canonical] = record
        return record

    def authorize(self, url: str, *, actor: str, capability: str) -> SourceRecord:
        if capability != "source_authorize":
            raise PermissionError("capability_denied:source_authorize")
        canonical = canonicalize(url)
        current = self._items[canonical]
        authorized = SourceRecord(
            url=current.url,
            proposed_by=current.proposed_by,
            authorized=True,
            profile_id=current.profile_id,
        )
        self._items[canonical] = authorized
        return authorized

    def is_authorized(self, url: str) -> bool:
        item = self._items.get(canonicalize(url))
        return bool(item and item.authorized)
