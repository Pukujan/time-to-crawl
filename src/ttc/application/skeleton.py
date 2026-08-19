from __future__ import annotations

import hashlib
from dataclasses import dataclass

from ttc.domain.identity import evidence_id_for, new_id
from ttc.domain.models import CrawlWork, Evidence, TypedRecord
from ttc.ports.catalog import OperationalCatalogPort
from ttc.ports.crawler import CrawlerEnginePort
from ttc.ports.evidence import EvidenceStorePort
from ttc.ports.extractor import ContentExtractorPort
from ttc.ports.identity import IdentityResolverPort
from ttc.ports.policy import PolicyDecisionPort
from ttc.ports.profiles import ProfileRegistryPort
from ttc.ports.query import QueryViewPort


@dataclass(frozen=True)
class SkeletonResult:
    profile_id: str
    run_id: str
    evidence_id: str
    record_ids: tuple[str, ...]
    records: tuple[TypedRecord, ...]


class WalkingSkeleton:
    def __init__(
        self,
        *,
        policy: PolicyDecisionPort,
        engine: CrawlerEnginePort,
        evidence: EvidenceStorePort,
        extractor: ContentExtractorPort,
        identity: IdentityResolverPort,
        catalog: OperationalCatalogPort,
        profiles: ProfileRegistryPort,
        query: QueryViewPort,
    ) -> None:
        self._policy = policy
        self._engine = engine
        self._evidence = evidence
        self._extractor = extractor
        self._identity = identity
        self._catalog = catalog
        self._profiles = profiles
        self._query = query

    def run(self, url: str, profile_id: str) -> SkeletonResult:
        profile = self._profiles.get(profile_id)
        decision = self._policy.authorize(url, profile_id=profile.profile_id)
        if not decision.allowed:
            raise PermissionError(decision.reason)
        run_id = new_id("run")
        crawled = self._engine.crawl(
            CrawlWork(url=decision.url, profile_id=profile.profile_id, run_id=run_id)
        )
        digest = hashlib.sha256(crawled.body).hexdigest()
        evidence = Evidence(
            evidence_id=evidence_id_for(digest),
            content_sha256=digest,
            fetched_url=crawled.final_url,
            captured_at=crawled.captured_at,
            content_type=crawled.content_type,
            body=crawled.body,
            engine_id=crawled.engine_id,
            engine_version=crawled.engine_version,
            profile_id=profile.profile_id,
            run_id=run_id,
        )
        stored = self._evidence.put(evidence)
        extracted = self._extractor.extract(stored, profile)
        resolved = self._identity.resolve(extracted)
        self._catalog.persist(resolved)
        return SkeletonResult(
            profile_id=profile.profile_id,
            run_id=run_id,
            evidence_id=stored.evidence_id,
            record_ids=tuple(record.record_id for record in resolved),
            records=resolved,
        )

    def query(self, profile_id: str) -> tuple[TypedRecord, ...]:
        return self._query.list_records(profile_id)
