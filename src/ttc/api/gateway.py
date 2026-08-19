from __future__ import annotations

from ttc.domain.models import TypedRecord
from ttc.ports.catalog import OperationalCatalogPort
from ttc.ports.profiles import ProfileRegistryPort


ALLOWED_ACTIONS = frozenset({"list_records", "get_profile", "source_propose"})


class BoundedGateway:
    def __init__(self, catalog: OperationalCatalogPort, profiles: ProfileRegistryPort) -> None:
        self._catalog = catalog
        self._profiles = profiles

    def invoke(self, action: str, **kwargs: object) -> object:
        if action not in ALLOWED_ACTIONS:
            raise PermissionError(f"action_denied:{action}")
        if action == "list_records":
            profile_id = str(kwargs["profile_id"])
            return self._catalog.list_by_profile(profile_id)
        if action == "get_profile":
            return self._profiles.get(str(kwargs["profile_id"]))
        raise PermissionError("source_propose_is_not_authorize")
