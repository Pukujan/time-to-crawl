from __future__ import annotations

import pytest

from ttc.adapters.sitemap import parse_sitemap


SITEMAP = b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/public</loc></url>
  <url><loc>http://127.0.0.1/admin</loc></url>
  <url><loc>http://169.254.169.254/latest/meta-data/</loc></url>
</urlset>
"""


def test_sitemap_parser_drops_forbidden_locs() -> None:
    urls = parse_sitemap(SITEMAP)
    assert urls == ("https://example.com/public",)


def test_invalid_sitemap_fails_closed() -> None:
    with pytest.raises(ValueError, match="invalid_sitemap"):
        parse_sitemap(b"<not-xml")
