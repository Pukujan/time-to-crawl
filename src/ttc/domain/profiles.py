from __future__ import annotations

from dataclasses import replace

from ttc.domain.models import Profile


def migrate_profile(profile: Profile, target_version: str) -> Profile:
    if profile.version == target_version:
        return profile
    if profile.version == "1.0.0" and target_version == "1.1.0":
        return replace(profile, version=target_version)
    raise ValueError(f"unsupported_migration:{profile.version}->{target_version}")


def deprecate_profile(profile: Profile) -> Profile:
    if profile.version.endswith("-deprecated"):
        return profile
    return replace(profile, version=f"{profile.version}-deprecated")
