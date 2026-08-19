from __future__ import annotations

from ttc.domain.concurrency import SlotPool
from ttc.domain.urls import canonicalize
from urllib.parse import urlparse


class HostSlotMap:
    def __init__(self, per_host: int = 1) -> None:
        self.per_host = per_host
        self._pools: dict[str, SlotPool] = {}

    def acquire(self, url: str) -> None:
        host = _host(url)
        pool = self._pools.setdefault(host, SlotPool(self.per_host))
        pool.acquire()

    def release(self, url: str) -> None:
        host = _host(url)
        self._pools.setdefault(host, SlotPool(self.per_host)).release()


def _host(url: str) -> str:
    parsed = urlparse(canonicalize(url))
    return parsed.hostname or url
