from __future__ import annotations

from ttc.domain.urls import canonicalize


def same_registrable_host(left: str, right: str) -> bool:
    a = canonicalize(left)
    b = canonicalize(right)
    host_a = a.split("://", 1)[-1].split("/", 1)[0].split(":")[0]
    host_b = b.split("://", 1)[-1].split("/", 1)[0].split(":")[0]
    return host_a == host_b and bool(host_a)
