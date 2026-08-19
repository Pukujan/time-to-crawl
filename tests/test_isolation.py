from __future__ import annotations

from ttc.domain.isolation import WorkerEnvelope, validate_worker


def test_worker_cannot_mount_host_secrets_or_admin() -> None:
    bad = WorkerEnvelope(
        identity="crawler",
        mounts=("HOME", "docker_socket", "postgres_admin"),
        network="host",
        secrets=("API_KEY",),
        rootless=False,
        read_only_root=False,
    )
    violations = validate_worker(bad)
    assert "forbidden_mount:HOME" in violations
    assert "host_network" in violations
    assert "worker_secrets" in violations
    assert "not_rootless" in violations


def test_isolated_worker_envelope_passes() -> None:
    good = WorkerEnvelope(
        identity="crawler",
        mounts=("scratch", "output"),
        network="none",
        secrets=(),
        rootless=True,
        read_only_root=True,
    )
    assert validate_worker(good) == ()
