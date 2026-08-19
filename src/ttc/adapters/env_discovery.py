from __future__ import annotations

import os

from ttc.domain.netpolicy import classify_url


class EnvDiscovery:
    """Reads allowlisted fixture URLs from env. Never calls a live search API."""

    def __init__(self, env_key: str) -> None:
        self.env_key = env_key

    def discover(self, query: str, *, profile_id: str) -> tuple[str, ...]:
        raw = os.environ.get(self.env_key, "")
        if not raw:
            return ()
        urls = []
        for item in raw.split(","):
            url = item.strip()
            if url and classify_url(url) == "public":
                urls.append(url)
        return tuple(urls)
