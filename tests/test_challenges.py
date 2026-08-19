from __future__ import annotations

import pytest

from ttc.domain.challenges import fail_closed_on_challenge, is_challenge


def test_captcha_and_forms_fail_closed() -> None:
    assert is_challenge("Please verify you are human")
    with pytest.raises(PermissionError, match="challenge_fail_closed"):
        fail_closed_on_challenge(b"cf-challenge")
    with pytest.raises(PermissionError, match="form_action_denied"):
        fail_closed_on_challenge('<form><input type="password">')
    fail_closed_on_challenge(b"ordinary listing html")
