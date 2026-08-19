from __future__ import annotations

from ttc.domain.isolation import WorkerEnvelope, validate_worker


def require_isolated(envelope: WorkerEnvelope) -> None:
    violations = validate_worker(envelope)
    if violations:
        raise PermissionError("worker_not_isolated:" + ",".join(violations))
