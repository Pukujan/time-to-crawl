from __future__ import annotations

import xml.etree.ElementTree as ET

from ttc.domain.netpolicy import classify_url


def parse_sitemap(blob: bytes) -> tuple[str, ...]:
    try:
        root = ET.fromstring(blob)
    except ET.ParseError as exc:
        raise ValueError("invalid_sitemap") from exc
    urls: list[str] = []
    for loc in root.iter():
        if loc.tag.endswith("loc") and loc.text:
            candidate = loc.text.strip()
            if classify_url(candidate) == "public":
                urls.append(candidate)
    return tuple(urls)
