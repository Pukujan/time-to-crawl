from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Conditional:
    etag: str | None
    last_modified: str | None


def should_revalidate(previous: Conditional | None, current: Conditional) -> bool:
    if previous is None:
        return True
    if current.etag and previous.etag and current.etag == previous.etag:
        return False
    if current.last_modified and previous.last_modified and current.last_modified == previous.last_modified:
        return False
    return True
