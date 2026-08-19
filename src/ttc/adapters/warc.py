from __future__ import annotations

from dataclasses import dataclass


WARC_VERSION = "WARC/1.1"


@dataclass(frozen=True)
class WarcRecord:
    record_type: str
    uri: str
    body: bytes
    content_type: str
    date: str


def write_warc(records: tuple[WarcRecord, ...]) -> bytes:
    chunks: list[bytes] = []
    for record in records:
        header = (
            f"{WARC_VERSION}\r\n"
            f"WARC-Type: {record.record_type}\r\n"
            f"WARC-Target-URI: {record.uri}\r\n"
            f"WARC-Date: {record.date}\r\n"
            f"Content-Type: {record.content_type}\r\n"
            f"Content-Length: {len(record.body)}\r\n"
            "\r\n"
        ).encode("utf-8")
        chunks.append(header + record.body + b"\r\n\r\n")
    return b"".join(chunks)


def read_warc(blob: bytes) -> tuple[WarcRecord, ...]:
    records: list[WarcRecord] = []
    remaining = blob
    marker = b"WARC/1.1\r\n"
    while remaining:
        remaining = remaining.lstrip(b"\r\n")
        if not remaining:
            break
        if not remaining.startswith(marker):
            raise ValueError("truncated_warc")
        header_end = remaining.find(b"\r\n\r\n")
        if header_end < 0:
            raise ValueError("truncated_warc")
        header = remaining[len(marker) : header_end].decode("utf-8")
        fields = {}
        for line in header.split("\r\n"):
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
        length = int(fields.get("Content-Length", "0"))
        start = header_end + 4
        end = start + length
        if end > len(remaining):
            raise ValueError("truncated_warc")
        body = remaining[start:end]
        records.append(
            WarcRecord(
                record_type=fields.get("WARC-Type", ""),
                uri=fields.get("WARC-Target-URI", ""),
                body=body,
                content_type=fields.get("Content-Type", "application/octet-stream"),
                date=fields.get("WARC-Date", ""),
            )
        )
        remaining = remaining[end:]
    return tuple(records)
