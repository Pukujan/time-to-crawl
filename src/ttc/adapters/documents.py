from __future__ import annotations

from ttc.domain.identity import new_id
from ttc.domain.models import Evidence, Profile, TypedRecord


class TextDocumentExtractor:
    def extract(self, evidence: Evidence, profile: Profile) -> tuple[TypedRecord, ...]:
        text = evidence.body.decode("utf-8", errors="replace")
        payload: dict[str, object] = {
            "text": text,
            "source_url": evidence.fetched_url,
            "content_type": evidence.content_type,
        }
        identity = "|".join(str(payload.get(key, evidence.fetched_url)) for key in profile.identity_keys)
        return (
            TypedRecord(
                record_id=new_id("rec"),
                profile_id=profile.profile_id,
                record_type=profile.profile_id,
                payload=payload,
                evidence_id=evidence.evidence_id,
                identity_key=identity,
            ),
        )
