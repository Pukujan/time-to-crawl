from __future__ import annotations

from ttc.domain.artifacts import Artifact, wrap


class MemoryObjectStore:
    """S3-shaped contract: put/get by original hash. No admin credentials."""

    def __init__(self, codec: object) -> None:
        self._codec = codec
        self._objects: dict[str, bytes] = {}
        self._meta: dict[str, Artifact] = {}

    def put(self, data: bytes) -> Artifact:
        artifact = wrap(data, self._codec)
        existing = self._objects.get(artifact.original_sha256)
        if existing is not None and existing != artifact.body_stored:
            restored = self._codec.decompress(existing)
            if restored != data:
                raise ValueError("object_conflict")
            return artifact
        self._objects[artifact.original_sha256] = artifact.body_stored
        self._meta[artifact.original_sha256] = artifact
        return artifact

    def get(self, original_sha256: str) -> bytes:
        stored = self._objects[original_sha256]
        restored = self._codec.decompress(stored)
        from ttc.domain.artifacts import original_sha256 as digest

        if digest(restored) != original_sha256:
            raise ValueError("integrity_failed")
        return restored
