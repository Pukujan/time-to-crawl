from __future__ import annotations

import ast
from pathlib import Path

from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.netpolicy import PolicyBroker, classify_url, is_forbidden_class

NETPOLICY = Path(__file__).resolve().parents[1] / "src" / "ttc" / "domain" / "netpolicy.py"


def test_encoded_loopback_is_forbidden() -> None:
    assert classify_url("http://2130706433/") != "public"
    assert is_forbidden_class(classify_url("http://0x7f000001/"))
    assert is_forbidden_class(classify_url("http://127.1/"))
    broker = PolicyBroker(frozenset({"http://2130706433/"}), DEFAULT_GRANTED)
    assert broker.authorize("http://2130706433/", profile_id="jobs").allowed is False


def test_ipv4_mapped_loopback_is_forbidden() -> None:
    assert is_forbidden_class(classify_url("http://[::ffff:127.0.0.1]/"))


def test_policy_source_does_not_invert_forbidden_check() -> None:
    tree = ast.parse(NETPOLICY.read_text(encoding="utf-8"))
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert "is_forbidden_class" in names
    source = NETPOLICY.read_text(encoding="utf-8")
    assert "if is_forbidden_class(network_class):" in source
    assert "if not is_forbidden_class(network_class):" not in source
