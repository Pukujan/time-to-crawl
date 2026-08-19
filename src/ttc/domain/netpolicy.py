from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse, unquote

from ttc.domain.models import PolicyDecision

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

INTEGER_HOST = re.compile(r"^(0x[0-9a-f]+|\d+)$", re.IGNORECASE)
DOTTED = re.compile(r"^[\d.]+$")


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
            parts = [int(part, 0) for part in name.split(".")]
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
    ) -> None:
        self._allowed_origins = allowed_origins
        self._granted = granted_capabilities

    def authorize(
        self,
        url: str,
        *,
        profile_id: str,
        requested_capabilities: tuple[str, ...] = (),
    ) -> PolicyDecision:
        network_class = classify_url(url)
        if is_forbidden_class(network_class):
            return PolicyDecision(
                allowed=False,
                url=url,
                reason=f"forbidden_network:{network_class}",
                robots_compliant=True,
            )
        origin = _origin(url)
        if origin not in self._allowed_origins and url not in self._allowed_origins:
            return PolicyDecision(
                allowed=False,
                url=url,
                reason="not_allowlisted",
                robots_compliant=True,
            )
        extra = set(requested_capabilities) - self._granted
        if extra:
            return PolicyDecision(
                allowed=False,
                url=url,
                reason="capability_denied:" + ",".join(sorted(extra)),
                robots_compliant=True,
            )
        return PolicyDecision(
            allowed=True,
            url=url,
            reason="allowlisted",
            robots_compliant=True,
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
