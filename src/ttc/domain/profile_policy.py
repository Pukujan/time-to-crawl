from __future__ import annotations

from ttc.domain.models import Profile


def refresh_interval(profile: Profile) -> int:
    if profile.refresh_interval_seconds < 1:
        return 86400
    return profile.refresh_interval_seconds
