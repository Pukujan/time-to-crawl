from __future__ import annotations

import pytest

from ttc.adapters.feeds import parse_feed

RSS = b"""<?xml version="1.0"?>
<rss><channel>
  <item><link>https://example.com/post</link></item>
  <item><link>http://127.0.0.1/admin</link></item>
</channel></rss>
"""


def test_feed_parser_drops_forbidden_links() -> None:
    assert parse_feed(RSS) == ("https://example.com/post",)


def test_invalid_feed_fails_closed() -> None:
    with pytest.raises(ValueError, match="invalid_feed"):
        parse_feed(b"<not-xml")
