from __future__ import annotations

import pytest

from ttc.application.worker import require_isolated
from ttc.domain.isolation import WorkerEnvelope


def test_isolated_worker_is_required_before_crawl() -> None:
    good = WorkerEnvelope(
        identity="crawler",
        mounts=("scratch", "output"),
        network="none",
        secrets=(),
        rootless=True,
        read_only_root=True,
    )
    require_isolated(good)
    bad = WorkerEnvelope(
        identity="crawler",
        mounts=("HOME",),
        network="host",
        secrets=("API_KEY",),
        rootless=False,
        read_only_root=False,
    )
    with pytest.raises(PermissionError, match="worker_not_isolated"):
        require_isolated(bad)
