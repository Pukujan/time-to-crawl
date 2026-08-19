from __future__ import annotations

import hashlib
from dataclasses import dataclass


def original_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Artifact:
    original_sha256: str
    original_size: int
    stored_sha256: str
    stored_size: int
    codec: str
    body_original: bytes
    body_stored: bytes


class IdentityCodec:
    name = "identity"

    def compress(self, data: bytes) -> bytes:
        return data

    def decompress(self, data: bytes) -> bytes:
        return data


def wrap(data: bytes, codec: IdentityCodec | object) -> Artifact:
    original = original_sha256(data)
    stored = codec.compress(data)
    restored = codec.decompress(stored)
    if restored != data:
        raise ValueError("codec_roundtrip_failed")
    return Artifact(
        original_sha256=original,
        original_size=len(data),
        stored_sha256=original_sha256(stored),
        stored_size=len(stored),
        codec=getattr(codec, "name", "unknown"),
        body_original=data,
        body_stored=stored,
    )
