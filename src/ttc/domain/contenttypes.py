from __future__ import annotations

from ttc.domain.models import Profile


def content_type_allowed(profile: Profile, content_type: str) -> bool:
    accepted = profile.allowed_content_types or ("application/json",)
    return any(content_type.startswith(item) for item in accepted)
