from __future__ import annotations

import json
from pathlib import Path

from ttc.domain.identity import new_id
from ttc.domain.models import (
    CrawlResult,
    CrawlWork,
    Evidence,
    PolicyDecision,
    Profile,
    TypedRecord,
)


FORBIDDEN_PROFILE_KEYS = frozenset(
    {"code", "script", "plugin", "entrypoint", "command", "executable"}
)


class AllowlistPolicy:
    def __init__(self, allowed: frozenset[str]) -> None:
        self._allowed = allowed

    def authorize(self, url: str, *, profile_id: str) -> PolicyDecision:
        if url in self._allowed:
            return PolicyDecision(
                allowed=True, url=url, reason="allowlisted", robots_compliant=True
            )
        return PolicyDecision(
            allowed=False, url=url, reason="not_allowlisted", robots_compliant=True
        )


class FakeCrawlerEngine:
    def __init__(self, fixtures: dict[str, Path], *, engine_id: str = "fake") -> None:
        self._fixtures = fixtures
        self.engine_id = engine_id

    def crawl(self, work: CrawlWork) -> CrawlResult:
        path = self._fixtures.get(work.url)
        if path is None:
            raise FileNotFoundError(work.url)
        return CrawlResult(
            requested_url=work.url,
            final_url=work.url,
            status=200,
            headers=(("content-type", "application/json"),),
            body=path.read_bytes(),
            content_type="application/json",
            captured_at="2026-08-19T00:00:00Z",
            engine_id=self.engine_id,
            engine_version="0.0.0-fake",
        )


class MemoryEvidenceStore:
    def __init__(self) -> None:
        self._items: dict[str, Evidence] = {}

    def put(self, evidence: Evidence) -> Evidence:
        existing = self._items.get(evidence.evidence_id)
        if existing is not None and existing.content_sha256 != evidence.content_sha256:
            raise ValueError("evidence_conflict")
        self._items[evidence.evidence_id] = evidence
        return evidence

    def get(self, evidence_id: str) -> Evidence:
        return self._items[evidence_id]


class MemoryCatalog:
    def __init__(self) -> None:
        self._items: dict[str, list[TypedRecord]] = {}

    def persist(self, records: tuple[TypedRecord, ...]) -> None:
        for record in records:
            self._items.setdefault(record.profile_id, []).append(record)

    def list_by_profile(self, profile_id: str) -> tuple[TypedRecord, ...]:
        return tuple(self._items.get(profile_id, ()))


class MemoryQuery:
    def __init__(self, catalog: MemoryCatalog) -> None:
        self._catalog = catalog

    def list_records(self, profile_id: str) -> tuple[TypedRecord, ...]:
        return self._catalog.list_by_profile(profile_id)


class FileProfileRegistry:
    def __init__(self, profiles: dict[str, Profile]) -> None:
        for profile in profiles.values():
            _reject_executable_profile(profile)
        self._profiles = profiles

    def get(self, profile_id: str) -> Profile:
        return self._profiles[profile_id]

    def list_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._profiles))


class SchemaGuidedExtractor:
    def extract(self, evidence: Evidence, profile: Profile) -> tuple[TypedRecord, ...]:
        payload = json.loads(evidence.body.decode("utf-8"))
        rows = payload if isinstance(payload, list) else payload.get("records", [payload])
        records: list[TypedRecord] = []
        for row in rows:
            identity = _identity_key(profile, row)
            records.append(
                TypedRecord(
                    record_id="pending",
                    profile_id=profile.profile_id,
                    record_type=row.get("record_type", profile.profile_id),
                    payload=row,
                    evidence_id=evidence.evidence_id,
                    identity_key=identity,
                )
            )
        return tuple(records)


class KeyIdentityResolver:
    def resolve(self, records: tuple[TypedRecord, ...]) -> tuple[TypedRecord, ...]:
        resolved: list[TypedRecord] = []
        for record in records:
            resolved.append(
                TypedRecord(
                    record_id=new_id("rec"),
                    profile_id=record.profile_id,
                    record_type=record.record_type,
                    payload=record.payload,
                    evidence_id=record.evidence_id,
                    identity_key=record.identity_key,
                )
            )
        return tuple(resolved)


class NullDiscovery:
    def discover(self, query: str, *, profile_id: str) -> tuple[str, ...]:
        return ()


class NullKnowledge:
    def record_lesson(self, profile_id: str, statement: str, evidence_id: str) -> str:
        return new_id("know")


def _identity_key(profile: Profile, row: dict[str, object]) -> str:
    parts = [str(row[key]) for key in profile.identity_keys]
    return "|".join(parts)


def _reject_executable_profile(profile: Profile) -> None:
    blob = json.dumps(profile.to_record())
    for key in FORBIDDEN_PROFILE_KEYS:
        if f'"{key}"' in blob:
            raise ValueError("executable_profile_forbidden")


def load_profile(path: Path) -> Profile:
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in FORBIDDEN_PROFILE_KEYS:
        if key in data:
            raise ValueError("executable_profile_forbidden")
    return Profile(
        profile_id=data["profile_id"],
        version=data["version"],
        title=data["title"],
        output_schema=data["output_schema"],
        identity_keys=tuple(data["identity_keys"]),
        requested_capabilities=tuple(data.get("requested_capabilities", ())),
    )
