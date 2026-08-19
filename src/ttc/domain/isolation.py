from __future__ import annotations

from dataclasses import dataclass


FORBIDDEN_WORKER_MOUNTS = (
    "HOME",
    "SSH",
    "browser_cookies",
    "dotenv",
    "docker_socket",
    "host_network",
    "postgres_admin",
    "object_store_admin",
)


@dataclass(frozen=True)
class WorkerEnvelope:
    identity: str
    mounts: tuple[str, ...]
    network: str
    secrets: tuple[str, ...]
    rootless: bool
    read_only_root: bool


def validate_worker(envelope: WorkerEnvelope) -> tuple[str, ...]:
    violations: list[str] = []
    for mount in envelope.mounts:
        if mount in FORBIDDEN_WORKER_MOUNTS:
            violations.append(f"forbidden_mount:{mount}")
    if envelope.network == "host":
        violations.append("host_network")
    if envelope.secrets:
        violations.append("worker_secrets")
    if not envelope.rootless:
        violations.append("not_rootless")
    if not envelope.read_only_root:
        violations.append("writable_root")
    return tuple(violations)
