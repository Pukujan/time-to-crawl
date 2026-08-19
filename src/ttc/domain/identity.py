from __future__ import annotations

import hashlib
import uuid


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def evidence_id_for(content_sha256: str) -> str:
    digest = hashlib.sha256(f"evidence:{content_sha256}".encode("utf-8")).hexdigest()
    return f"ev_{digest[:32]}"
