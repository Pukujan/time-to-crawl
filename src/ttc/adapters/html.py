from __future__ import annotations

import json
import re
from html.parser import HTMLParser

from ttc.domain.identity import new_id
from ttc.domain.models import Evidence, Profile, TypedRecord


class _TextCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._json_ld: list[str] = []
        self._in_script = False
        self._script_type = ""
        self.title = ""
        self._capture_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        mapping = {key: value for key, value in attrs}
        if tag == "title":
            self._capture_title = True
        if tag == "script" and mapping.get("type") == "application/ld+json":
            self._in_script = True
            self._script_type = "ld+json"

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._capture_title = False
        if tag == "script":
            self._in_script = False
            self._script_type = ""

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self.title += data.strip()
        if self._in_script and self._script_type == "ld+json":
            self._json_ld.append(data)
        else:
            self._chunks.append(data)

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self._chunks)).strip()

    @property
    def json_ld(self) -> list[object]:
        parsed: list[object] = []
        for blob in self._json_ld:
            try:
                parsed.append(json.loads(blob))
            except json.JSONDecodeError:
                continue
        return parsed


class HtmlExtractor:
    def extract(self, evidence: Evidence, profile: Profile) -> tuple[TypedRecord, ...]:
        if evidence.content_type.startswith("application/json"):
            from ttc.adapters.memory import SchemaGuidedExtractor

            return SchemaGuidedExtractor().extract(evidence, profile)
        parser = _TextCollector()
        parser.feed(evidence.body.decode("utf-8", errors="replace"))
        payload: dict[str, object] = {"title": parser.title, "text": parser.text}
        if parser.json_ld:
            payload["json_ld"] = parser.json_ld[0]
            if isinstance(parser.json_ld[0], dict):
                payload.update(
                    {
                        key: value
                        for key, value in parser.json_ld[0].items()
                        if key in profile.identity_keys or key in {"name", "title"}
                    }
                )
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
