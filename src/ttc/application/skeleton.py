from __future__ import annotations

import hashlib
from dataclasses import dataclass

from ttc.application.budgeting import consume_result
from ttc.domain.budget import Budget, BudgetTracker
from ttc.domain.challenges import fail_closed_on_challenge
from ttc.domain.contenttypes import content_type_allowed
from ttc.domain.limits import max_redirects_ok
from ttc.domain.identity import evidence_id_for, new_id
from ttc.domain.models import CrawlWork, Evidence, TypedRecord
from ttc.domain.provenance import ProvenanceLink, bind
from ttc.domain.redirects import detect_redirect_loop
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
    provenance: tuple[ProvenanceLink, ...]
    outlinks: tuple[str, ...]


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
        budget: Budget | None = None,
    ) -> None:
        self._policy = policy
        self._engine = engine
        self._evidence = evidence
        self._extractor = extractor
        self._identity = identity
        self._catalog = catalog
        self._profiles = profiles
        self._query = query
        self._budget = BudgetTracker(budget or Budget(32, 2_000_000, 2, 60))

    def run(self, url: str, profile_id: str) -> SkeletonResult:
        profile = self._profiles.get(profile_id)
        decision = self._policy.authorize(
            url,
            profile_id=profile.profile_id,
            requested_capabilities=profile.requested_capabilities,
        )
        if not decision.allowed:
            raise PermissionError(decision.reason)
        run_id = new_id("run")
        crawled = self._engine.crawl(
            CrawlWork(url=decision.url, profile_id=profile.profile_id, run_id=run_id)
        )
        if not max_redirects_ok(crawled):
            raise PermissionError("too_many_redirects")
        consume_result(self._budget, crawled)
        hops = crawled.redirect_chain
        if not hops or hops[-1] != crawled.final_url:
            hops = hops + (crawled.final_url,)
        self._budget.consume(depth=max(0, len(hops) - 1))
        for hop in hops:
            hop_decision = self._policy.authorize(
                hop,
                profile_id=profile.profile_id,
                requested_capabilities=profile.requested_capabilities,
            )
            if not hop_decision.allowed:
                raise PermissionError(hop_decision.reason)
        if detect_redirect_loop(hops):
            raise PermissionError("redirect_loop")
        authorized_outlinks: list[str] = []
        for outlink in crawled.outlinks:
            out_decision = self._policy.authorize(
                outlink,
                profile_id=profile.profile_id,
                requested_capabilities=profile.requested_capabilities,
            )
            if out_decision.allowed:
                authorized_outlinks.append(outlink)
        fail_closed_on_challenge(crawled.body)
        if not crawled.body:
            raise PermissionError("empty_body")
        if not content_type_allowed(profile, crawled.content_type):
            raise PermissionError("content_type_denied")
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
        provenance = tuple(
            bind(
                record_id=record.record_id,
                evidence_id=stored.evidence_id,
                engine_id=crawled.engine_id,
                engine_version=crawled.engine_version,
                profile_id=profile.profile_id,
                run_id=run_id,
                fetched_url=crawled.final_url,
                policy_reason=decision.reason,
            )
            for record in resolved
        )
        return SkeletonResult(
            profile_id=profile.profile_id,
            run_id=run_id,
            evidence_id=stored.evidence_id,
            record_ids=tuple(record.record_id for record in resolved),
            records=resolved,
            provenance=provenance,
            outlinks=tuple(authorized_outlinks),
        )

    def query(self, profile_id: str) -> tuple[TypedRecord, ...]:
        return self._query.list_records(profile_id)
