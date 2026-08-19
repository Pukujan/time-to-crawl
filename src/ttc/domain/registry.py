from __future__ import annotations

from dataclasses import dataclass

from ttc.domain.netpolicy import classify_url, is_forbidden_class


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
        network_class = classify_url(url)
        if is_forbidden_class(network_class):
            raise PermissionError(f"forbidden_network:{network_class}")
        record = SourceRecord(
            url=url,
            proposed_by=proposed_by,
            authorized=False,
            profile_id=profile_id,
        )
        self._items[url] = record
        return record

    def authorize(self, url: str, *, actor: str, capability: str) -> SourceRecord:
        if capability != "source_authorize":
            raise PermissionError("capability_denied:source_authorize")
        current = self._items[url]
        authorized = SourceRecord(
            url=current.url,
            proposed_by=current.proposed_by,
            authorized=True,
            profile_id=current.profile_id,
        )
        self._items[url] = authorized
        return authorized

    def is_authorized(self, url: str) -> bool:
        item = self._items.get(url)
        return bool(item and item.authorized)
