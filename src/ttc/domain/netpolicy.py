from __future__ import annotations

import ipaddress
import re
from typing import Protocol
from urllib.parse import urlparse, unquote

from ttc.domain.capabilities import KNOWN_CAPABILITIES
from ttc.domain.models import PolicyDecision
from ttc.domain.robots import path_of, robots_allows
from ttc.domain.urls import canonicalize


class _SourceAuth(Protocol):
    def is_authorized(self, url: str) -> bool: ...


class _RobotsLookup(Protocol):
    def allows(self, origin: str, path: str) -> bool: ...

FORBIDDEN_HOSTS = frozenset(
    {
        "localhost",
        "localhost.localdomain",
        "metadata.google.internal",
        "metadata.internal",
        "instance-data",
    }
)

METADATA_IPS = frozenset(
    {
        ipaddress.ip_address("169.254.169.254"),
        ipaddress.ip_address("fd00:ec2::254"),
    }
)

INTEGER_HOST = re.compile(r"^(0x[0-9a-f]+|0[0-7]+|\d+)$", re.IGNORECASE)
DOTTED = re.compile(r"^[0-9a-fx.]+$", re.IGNORECASE)


def _parse_ip(host: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    name = host.strip().lower().rstrip(".")
    if "%" in name:
        name = name.split("%", 1)[0]
    if name.startswith("[") and name.endswith("]"):
        name = name[1:-1]
    try:
        ip = ipaddress.ip_address(name)
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
            return ip.ipv4_mapped
        if isinstance(ip, ipaddress.IPv6Address) and ip.teredo:
            return None
        return ip
    except ValueError:
        pass
    if INTEGER_HOST.match(name):
        try:
            value = int(name, 0)
            if 0 <= value <= 2**32 - 1:
                return ipaddress.IPv4Address(value)
        except ValueError:
            return None
    if DOTTED.match(name):
        try:
            parts = [_int_part(part) for part in name.split(".")]
            if any(part < 0 for part in parts):
                return None
            if len(parts) == 4 and all(part <= 255 for part in parts):
                return ipaddress.IPv4Address(bytes(parts))
            if len(parts) == 1 and parts[0] <= 2**32 - 1:
                return ipaddress.IPv4Address(parts[0])
            if len(parts) == 2 and parts[0] <= 255 and parts[1] <= 2**24 - 1:
                return ipaddress.IPv4Address((parts[0] << 24) + parts[1])
            if len(parts) == 3 and parts[0] <= 255 and parts[1] <= 255 and parts[2] <= 2**16 - 1:
                return ipaddress.IPv4Address((parts[0] << 24) + (parts[1] << 16) + parts[2])
        except ValueError:
            return None
    return None


def _int_part(part: str) -> int:
    if part.startswith("0x"):
        return int(part, 16)
    if part.startswith("0") and len(part) > 1 and all(ch in "01234567" for ch in part):
        return int(part, 8)
    return int(part, 10)


def classify_host(host: str) -> str:
    name = unquote(host.strip()).lower().rstrip(".")
    if "%" in name and not name.startswith("["):
        name = name.split("%", 1)[0]
    if name.startswith("[") and name.endswith("]"):
        name = name[1:-1]
    if name in FORBIDDEN_HOSTS:
        return "loopback" if name.startswith("localhost") else "metadata"
    ip = _parse_ip(name)
    if ip is None:
        return "public"
    if ip in METADATA_IPS:
        return "metadata"
    if ip.is_loopback:
        return "loopback"
    if ip.is_link_local:
        return "link_local"
    if ip.is_unspecified:
        return "unspecified"
    if ip.is_multicast:
        return "multicast"
    if ip.is_private or ip.is_reserved:
        return "private"
    return "public"


def classify_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return "disallowed_scheme"
    host = parsed.hostname or ""
    if not host:
        return "missing_host"
    return classify_host(host)


def is_forbidden_class(network_class: str) -> bool:
    return network_class != "public"


class PolicyBroker:
    def __init__(
        self,
        allowed_origins: frozenset[str],
        granted_capabilities: frozenset[str],
        robots_txt: str | None = None,
        source_registry: _SourceAuth | None = None,
        require_source_auth: bool = False,
        robots_lookup: _RobotsLookup | None = None,
    ) -> None:
        self._allowed_origins = allowed_origins
        self._granted = granted_capabilities
        self._robots_txt = robots_txt
        self._source_registry = source_registry
        self._require_source_auth = require_source_auth
        self._robots_lookup = robots_lookup

    def authorize(
        self,
        url: str,
        *,
        profile_id: str,
        requested_capabilities: tuple[str, ...] = (),
    ) -> PolicyDecision:
        canonical = canonicalize(url)
        network_class = classify_url(canonical)
        if is_forbidden_class(network_class):
            return PolicyDecision(
                allowed=False,
                url=canonical,
                reason=f"forbidden_network:{network_class}",
                robots_compliant=True,
            )
        origin = _origin(canonical)
        if origin not in self._allowed_origins and canonical not in self._allowed_origins and url not in self._allowed_origins:
            return PolicyDecision(
                allowed=False,
                url=url,
                reason="not_allowlisted",
                robots_compliant=True,
            )
        unknown = set(requested_capabilities) - KNOWN_CAPABILITIES
        if unknown:
            return PolicyDecision(
                allowed=False,
                url=canonical,
                reason="unknown_capability:" + ",".join(sorted(unknown)),
                robots_compliant=True,
            )
        extra = set(requested_capabilities) - self._granted
        if extra:
            return PolicyDecision(
                allowed=False,
                url=canonical,
                reason="capability_denied:" + ",".join(sorted(extra)),
                robots_compliant=True,
            )
        if self._require_source_auth:
            if self._source_registry is None or not self._source_registry.is_authorized(canonical):
                return PolicyDecision(
                    allowed=False,
                    url=canonical,
                    reason="source_unauthorized",
                    robots_compliant=True,
                )
        robots_ok = True
        if self._robots_lookup is not None:
            robots_ok = self._robots_lookup.allows(origin, path_of(canonical))
        elif self._robots_txt is not None:
            robots_ok = robots_allows(self._robots_txt, path_of(canonical))
        if not robots_ok:
            return PolicyDecision(
                allowed=False,
                url=canonical,
                reason="robots_disallow",
                robots_compliant=False,
            )
        return PolicyDecision(
            allowed=True,
            url=canonical,
            reason="allowlisted",
            robots_compliant=robots_ok,
        )

    def authorize_chain(self, urls: tuple[str, ...], *, profile_id: str) -> PolicyDecision:
        if not urls:
            return PolicyDecision(allowed=False, url="", reason="empty_chain")
        for hop in urls:
            decision = self.authorize(hop, profile_id=profile_id)
            if not decision.allowed:
                return decision
        return PolicyDecision(allowed=True, url=urls[-1], reason="chain_allowed")


def _origin(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    return f"{parsed.scheme}://{parsed.netloc}"
