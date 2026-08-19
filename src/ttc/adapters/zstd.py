from __future__ import annotations

import hashlib

from ttc.domain.artifacts import Artifact, original_sha256


class ZstdCodec:
    name = "zstd"

    def __init__(self, level: int = 3) -> None:
        self.level = level

    def compress(self, data: bytes) -> bytes:
        try:
            import zstandard
        except ImportError as exc:
            raise RuntimeError("zstandard_required") from exc
        return zstandard.ZstdCompressor(level=self.level).compress(data)

    def decompress(self, data: bytes) -> bytes:
        try:
            import zstandard
        except ImportError as exc:
            raise RuntimeError("zstandard_required") from exc
        return zstandard.ZstdDecompressor().decompress(data)


def wrap_zstd(data: bytes) -> Artifact:
    from ttc.domain.artifacts import wrap

    return wrap(data, ZstdCodec())


def stored_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assert_original_identity(artifact: Artifact, original: bytes) -> None:
    if artifact.original_sha256 != original_sha256(original):
        raise ValueError("identity_drift")
