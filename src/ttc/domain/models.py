from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    url: str
    reason: str
    robots_compliant: bool = True


@dataclass(frozen=True)
class CrawlWork:
    url: str
    profile_id: str
    run_id: str


@dataclass(frozen=True)
class CrawlResult:
    requested_url: str
    final_url: str
    status: int
    headers: tuple[tuple[str, str], ...]
    body: bytes
    content_type: str
    captured_at: str
    engine_id: str
    engine_version: str
    outlinks: tuple[str, ...] = ()
    redirect_chain: tuple[str, ...] = ()


@dataclass(frozen=True)
class Profile:
    profile_id: str
    version: str
    title: str
    output_schema: str
    identity_keys: tuple[str, ...]
    requested_capabilities: tuple[str, ...] = ()
    allowed_content_types: tuple[str, ...] = ("application/json",)
    refresh_interval_seconds: int = 86400

    def to_record(self) -> dict[str, object]:
        return {
            "schema_version": "ttc.profile.v1",
            "profile_id": self.profile_id,
            "version": self.version,
            "title": self.title,
            "output_schema": self.output_schema,
            "identity_keys": list(self.identity_keys),
            "requested_capabilities": list(self.requested_capabilities),
            "allowed_content_types": list(self.allowed_content_types),
            "refresh_interval_seconds": self.refresh_interval_seconds,
        }


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    content_sha256: str
    fetched_url: str
    captured_at: str
    content_type: str
    body: bytes
    engine_id: str
    engine_version: str
    profile_id: str
    run_id: str
    headers: tuple[tuple[str, str], ...] = ()

    def to_record(self) -> dict[str, object]:
        return {
            "schema_version": "ttc.evidence.v1",
            "evidence_id": self.evidence_id,
            "content_sha256": self.content_sha256,
            "fetched_url": self.fetched_url,
            "captured_at": self.captured_at,
            "content_type": self.content_type,
            "engine_id": self.engine_id,
            "engine_version": self.engine_version,
            "profile_id": self.profile_id,
            "run_id": self.run_id,
            "headers": [list(item) for item in self.headers],
        }


@dataclass(frozen=True)
class TypedRecord:
    record_id: str
    profile_id: str
    record_type: str
    payload: dict[str, object]
    evidence_id: str
    identity_key: str

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_id, str) or not self.evidence_id:
            raise TypeError("evidence_id_required")

    def to_record(self) -> dict[str, object]:
        return {
            "schema_version": "ttc.typed-record.v1",
            "record_id": self.record_id,
            "profile_id": self.profile_id,
            "record_type": self.record_type,
            "payload": self.payload,
            "evidence_id": self.evidence_id,
            "identity_key": self.identity_key,
        }
