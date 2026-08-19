from __future__ import annotations

import xml.etree.ElementTree as ET

from ttc.domain.netpolicy import classify_url


def parse_feed(blob: bytes) -> tuple[str, ...]:
    try:
        root = ET.fromstring(blob)
    except ET.ParseError as exc:
        raise ValueError("invalid_feed") from exc
    urls: list[str] = []
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1].lower()
        if tag in {"link", "guid", "loc"}:
            href = (node.attrib.get("href") or node.text or "").strip()
            if href and classify_url(href) == "public":
                urls.append(href)
    return tuple(dict.fromkeys(urls))
