"""Fail-closed password gate for the local ShopGuard Streamlit application."""
from __future__ import annotations

import hmac
from collections.abc import Mapping, MutableMapping
from typing import Any

AUTH_KEY = "shopguard_authenticated"


def configured_password(secrets: Mapping[str, Any]) -> str | None:
    """Return a non-empty application password, otherwise signal unavailable configuration."""
    value = secrets.get("APP_PASSWORD")
    return value if isinstance(value, str) and value.strip() else None


def is_authenticated(session_state: Mapping[str, Any]) -> bool:
    """Read authentication state without treating an absent key as access."""
    return session_state.get(AUTH_KEY) is True


def authenticate(session_state: MutableMapping[str, Any], expected_password: str | None, supplied_password: str) -> bool:
    """Compare password safely and persist only a boolean authenticated state."""
    success = bool(expected_password) and hmac.compare_digest(expected_password, supplied_password)
    session_state[AUTH_KEY] = success
    return success


def logout(session_state: MutableMapping[str, Any]) -> None:
    """Clear the session authentication marker."""
    session_state.pop(AUTH_KEY, None)


LOGIN_STYLES = """
<style>
.login-card { background: #ffffff; border: 1px solid #c9d7e7; border-radius: 14px;
              box-shadow: 0 6px 20px rgba(20, 60, 100, .12); padding: 2rem; margin-top: 5rem; }
.login-brand { color: #12355b !important; text-align: center; margin-bottom: .25rem; }
.login-copy { color: #52677f !important; text-align: center; margin-bottom: 1.25rem; }
</style>
"""


def require_authentication() -> None:
    """Render the password screen or stop the page before protected content renders."""
    import streamlit as st

    try:
        password = configured_password(st.secrets)
    except Exception:
        # Missing or unreadable Streamlit secrets must never open the application.
        password = None
    if password is None:
        st.markdown(LOGIN_STYLES, unsafe_allow_html=True)
        st.error("ShopGuard is not configured for access. Set a non-empty APP_PASSWORD in Streamlit secrets, then restart the app.")
        st.stop()

    if is_authenticated(st.session_state):
        if st.sidebar.button("Logout", key="shopguard_logout", use_container_width=True):
            logout(st.session_state)
            st.rerun()
        return

    left, center, right = st.columns([1, 1.25, 1])
    with center:
        st.markdown(LOGIN_STYLES + "<div class='login-card'><h1 class='login-brand'>🛡️ ShopGuard</h1><p class='login-copy'>Sign in to access the product image watermarking workspace.</p></div>", unsafe_allow_html=True)
        with st.form("shopguard_login_form"):
            supplied_password = st.text_input("Password", type="password", autocomplete="current-password")
            submitted = st.form_submit_button("Login", use_container_width=True)
        if submitted:
            if authenticate(st.session_state, password, supplied_password):
                st.rerun()
            else:
                st.error("Incorrect password. Try again.")
    st.stop()
