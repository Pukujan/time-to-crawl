from __future__ import annotations

import json
from pathlib import Path

from ttc.domain.artifacts import Artifact, wrap
from ttc.domain.identity import evidence_id_for
from ttc.domain.models import Evidence


class ContentAddressedStore:
    def __init__(self, root: Path, codec: object) -> None:
        self._root = root
        self._codec = codec
        self._root.mkdir(parents=True, exist_ok=True)

    def put_bytes(self, data: bytes) -> Artifact:
        artifact = wrap(data, self._codec)
        blob = self._path(artifact.original_sha256)
        blob.parent.mkdir(parents=True, exist_ok=True)
        meta = blob.with_suffix(".json")
        if blob.exists():
            stored = blob.read_bytes()
            if wrap(data, self._codec).stored_sha256 != _sha(stored) and stored != artifact.body_stored:
                restored = self._codec.decompress(stored)
                if restored != data:
                    raise ValueError("artifact_conflict")
            return artifact
        tmp = blob.with_suffix(".tmp")
        tmp.write_bytes(artifact.body_stored)
        tmp.replace(blob)
        meta.write_text(
            json.dumps(
                {
                    "original_sha256": artifact.original_sha256,
                    "original_size": artifact.original_size,
                    "stored_sha256": artifact.stored_sha256,
                    "stored_size": artifact.stored_size,
                    "codec": artifact.codec,
                }
            ),
            encoding="utf-8",
        )
        restored = self._codec.decompress(blob.read_bytes())
        if restored != data:
            raise ValueError("integrity_failed")
        return artifact

    def put_evidence(self, evidence: Evidence) -> Evidence:
        from ttc.domain.artifacts import original_sha256 as digest

        if digest(evidence.body) != evidence.content_sha256:
            raise ValueError("hash_mismatch")
        if evidence.evidence_id != evidence_id_for(evidence.content_sha256):
            raise ValueError("identity_mismatch")
        self.put_bytes(evidence.body)
        return evidence

    def get_bytes(self, original_sha256: str) -> bytes:
        blob = self._path(original_sha256)
        meta = json.loads(blob.with_suffix(".json").read_text(encoding="utf-8"))
        stored = blob.read_bytes()
        restored = self._codec.decompress(stored)
        from ttc.domain.artifacts import original_sha256 as digest

        if digest(restored) != original_sha256 or digest(restored) != meta["original_sha256"]:
            raise ValueError("integrity_failed")
        return restored

    def _path(self, original_sha256: str) -> Path:
        return self._root / original_sha256[:2] / original_sha256


def _sha(data: bytes) -> str:
    from ttc.domain.artifacts import original_sha256

    return original_sha256(data)
