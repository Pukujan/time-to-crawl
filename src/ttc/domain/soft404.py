from __future__ import annotations

from ttc.domain.failures import classify_status
from ttc.domain.models import CrawlResult


def is_soft_404(result: CrawlResult) -> bool:
    if classify_status(result.status) != "success":
        return False
    sample = result.body[:2048].lower()
    if len(result.body) >= 2048:
        return False
    title_404 = b"<title>" in sample and b"404" in sample
    if title_404:
        return True
    return b"not found" in sample or b"page not found" in sample
