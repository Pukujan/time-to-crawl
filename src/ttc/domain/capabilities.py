from __future__ import annotations

KNOWN_CAPABILITIES = frozenset(
    {
        "profile_read",
        "fetch_public",
        "source_discover",
        "source_authorize",
        "authenticated_session",
        "form_action",
        "anti_block",
        "knowledge_propose",
        "ops_admin",
    }
)

DEFAULT_GRANTED = frozenset({"profile_read", "fetch_public"})


def profile_cannot_grant(requested: tuple[str, ...], granted: frozenset[str]) -> frozenset[str]:
    return frozenset(requested) - granted
