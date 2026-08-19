from __future__ import annotations

from ttc.domain.conditional import Conditional, should_revalidate


def test_matching_etag_does_not_mean_never_refresh() -> None:
    previous = Conditional(etag='"abc"', last_modified="Mon, 01 Jan 2026 00:00:00 GMT")
    same = Conditional(etag='"abc"', last_modified="Mon, 01 Jan 2026 00:00:00 GMT")
    changed = Conditional(etag='"def"', last_modified="Tue, 02 Jan 2026 00:00:00 GMT")
    assert should_revalidate(previous, same) is False
    assert should_revalidate(previous, changed) is True
    assert should_revalidate(None, same) is True
