from __future__ import annotations

from ttc.adapters.objectstore import MemoryObjectStore
from ttc.adapters.zstd import ZstdCodec
from ttc.domain.artifacts import original_sha256


def test_object_store_roundtrip_and_dedup() -> None:
    store = MemoryObjectStore(ZstdCodec())
    payload = b"object-bytes" * 32
    first = store.put(payload)
    second = store.put(payload)
    assert first.original_sha256 == second.original_sha256 == original_sha256(payload)
    assert store.get(first.original_sha256) == payload
