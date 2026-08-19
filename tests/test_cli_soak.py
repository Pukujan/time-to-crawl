from __future__ import annotations

from ttc.cli import main


def test_soak_command_is_fixture_only(capsys) -> None:
    main(["soak", "3"])
    out = capsys.readouterr().out
    assert '"cycles": 3' in out
    assert '"live_crawl": false' in out
