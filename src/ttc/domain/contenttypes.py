from __future__ import annotations

from ttc.domain.models import Profile


def content_type_allowed(profile: Profile, content_type: str) -> bool:
    allowed = {
        "products-and-offers": ("application/json", "text/html"),
        "jobs": ("application/json", "text/html"),
        "inference-providers": ("application/json", "text/html"),
        "legal-documents": ("application/json", "text/html", "text/plain", "application/pdf"),
    }
    accepted = allowed.get(profile.profile_id, ("application/json",))
    return any(content_type.startswith(item) for item in accepted)
