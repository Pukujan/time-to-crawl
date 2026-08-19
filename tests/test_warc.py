from __future__ import annotations

import pytest

from ttc.adapters.warc import WarcRecord, read_warc, write_warc


def test_warc_roundtrip() -> None:
    record = WarcRecord(
        record_type="response",
        uri="https://example.com/x",
        body=b"hello",
        content_type="text/plain",
        date="2026-08-19T00:00:00Z",
    )
    blob = write_warc((record,))
    restored = read_warc(blob)
    assert restored == (record,)
    assert blob.startswith(b"WARC/1.1")


def test_truncated_warc_fails_closed() -> None:
    blob = write_warc(
        (
            WarcRecord(
                record_type="response",
                uri="https://example.com/x",
                body=b"hello-world",
                content_type="text/plain",
                date="2026-08-19T00:00:00Z",
            ),
        )
    )
    with pytest.raises(ValueError, match="truncated_warc"):
        read_warc(blob[: len(blob) // 2])
