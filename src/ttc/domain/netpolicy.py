from __future__ import annotations

import ipaddress
from urllib.parse import urlparse

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

METADATA_IPS = frozenset({"169.254.169.254", "fd00:ec2::254"})


def classify_host(host: str) -> str:
    name = host.strip().lower().rstrip(".")
    if "%" in name:
        name = name.split("%", 1)[0]
    if name.startswith("[") and name.endswith("]"):
        name = name[1:-1]
    if name in FORBIDDEN_HOSTS:
        return "loopback" if name.startswith("localhost") else "metadata"
    if name in METADATA_IPS:
        return "metadata"
    try:
        ip = ipaddress.ip_address(name)
    except ValueError:
        return "public"
    if ip.is_loopback:
        return "loopback"
    if ip.is_link_local or str(ip) in METADATA_IPS:
        return "metadata" if str(ip) in METADATA_IPS else "link_local"
    if ip.is_private or ip.is_reserved or ip.is_unspecified or ip.is_multicast:
        if ip.is_unspecified:
            return "unspecified"
        if ip.is_multicast:
            return "multicast"
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
