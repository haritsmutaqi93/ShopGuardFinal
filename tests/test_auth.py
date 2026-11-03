from backend.auth import AUTH_KEY, authenticate, configured_password, is_authenticated, logout


def test_unauthenticated_session_is_denied():
    assert not is_authenticated({})


def test_missing_password_configuration_is_not_usable():
    assert configured_password({}) is None
    assert configured_password({"APP_PASSWORD": "   "}) is None


def test_successful_login_marks_session_authenticated():
    session: dict = {}
    assert authenticate(session, "correct-horse", "correct-horse")
    assert is_authenticated(session)
    assert session[AUTH_KEY] is True


def test_incorrect_login_does_not_authenticate():
    session: dict = {}
    assert not authenticate(session, "correct-horse", "wrong-password")
    assert not is_authenticated(session)


def test_logout_clears_authentication():
    session = {AUTH_KEY: True}
    logout(session)
    assert not is_authenticated(session)
