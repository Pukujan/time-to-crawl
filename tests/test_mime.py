from __future__ import annotations

from ttc.domain.mime import declared_matches_body


def test_json_content_type_requires_json_body() -> None:
    assert declared_matches_body("application/json", b'{"ok": true}')
    assert declared_matches_body("application/json; charset=utf-8", b"[1]")
    assert not declared_matches_body("application/json", b"<html></html>")


def test_html_and_pdf_magic() -> None:
    assert declared_matches_body("text/html", b"<!doctype html><title>x</title>")
    assert declared_matches_body("application/pdf", b"%PDF-1.4")
    assert not declared_matches_body("application/pdf", b"not a pdf")
