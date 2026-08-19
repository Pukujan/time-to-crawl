from __future__ import annotations


def declared_matches_body(content_type: str, body: bytes) -> bool:
    lowered = content_type.split(";", 1)[0].strip().lower()
    if lowered in {"application/json", "text/json"}:
        stripped = body.lstrip()
        return stripped.startswith(b"{") or stripped.startswith(b"[")
    if lowered == "text/html":
        sample = body.lstrip()[:64].lower()
        return b"<html" in sample or b"<!doctype" in sample or b"<title" in sample
    if lowered == "application/pdf":
        return body.startswith(b"%PDF")
    if lowered.startswith("text/"):
        return True
    return True
