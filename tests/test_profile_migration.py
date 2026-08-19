from __future__ import annotations

import pytest

from ttc.adapters.memory import load_profile
from ttc.domain.profiles import deprecate_profile, migrate_profile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_profile_migration_and_deprecation() -> None:
    profile = load_profile(ROOT / "contracts" / "profiles" / "jobs.v1.json")
    migrated = migrate_profile(profile, "1.1.0")
    assert migrated.version == "1.1.0"
    assert migrated.profile_id == profile.profile_id
    deprecated = deprecate_profile(migrated)
    assert deprecated.version.endswith("-deprecated")
    with pytest.raises(ValueError, match="unsupported_migration"):
        migrate_profile(profile, "9.9.9")
