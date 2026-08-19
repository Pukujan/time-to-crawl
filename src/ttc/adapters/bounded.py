from __future__ import annotations

MAX_DECOMPRESSED = 10 * 1024 * 1024


class BoundedCodec:
    def __init__(self, inner: object, *, max_bytes: int = MAX_DECOMPRESSED) -> None:
        self._inner = inner
        self.max_bytes = max_bytes
        self.name = getattr(inner, "name", "bounded")

    def compress(self, data: bytes) -> bytes:
        if len(data) > self.max_bytes:
            raise ValueError("resource_bomb")
        return self._inner.compress(data)

    def decompress(self, data: bytes) -> bytes:
        restored = self._inner.decompress(data)
        if len(restored) > self.max_bytes:
            raise ValueError("resource_bomb")
        return restored
