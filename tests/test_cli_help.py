from __future__ import annotations

import pytest

from ttc.cli import main


def test_help_lists_fixture_commands(capsys) -> None:
    main(["help"])
    out = capsys.readouterr().out
    assert "status" in out
    assert "soak" in out
    assert "live_crawl" in out


def test_unknown_command_fails_closed() -> None:
    with pytest.raises(PermissionError, match="unknown_command"):
        main(["browser"])
    with pytest.raises(PermissionError, match="unknown_command"):
        main(["fetch"])
