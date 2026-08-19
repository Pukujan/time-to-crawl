from __future__ import annotations

import pytest

from ttc.adapters.bounded import BoundedCodec
from ttc.domain.artifacts import IdentityCodec


def test_bounded_codec_rejects_resource_bomb() -> None:
    codec = BoundedCodec(IdentityCodec(), max_bytes=8)
    with pytest.raises(ValueError, match="resource_bomb"):
        codec.compress(b"0123456789")
    with pytest.raises(ValueError, match="resource_bomb"):
        codec.decompress(b"0123456789")
    assert codec.compress(b"ok") == b"ok"
