from __future__ import annotations

from ttc.cli import main


def test_profiles_command_lists_reference_profiles(capsys) -> None:
    main(["profiles"])
    out = capsys.readouterr().out
    assert "products-and-offers" in out
    assert "jobs" in out
    assert "inference-providers" in out
    assert "legal-documents" in out
    assert "max_depth" in out
    assert "requested_capabilities" in out
