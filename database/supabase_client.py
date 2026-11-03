"""Lazy, server-side-only Supabase client configuration."""
from __future__ import annotations

from typing import Any


class SupabaseConfigurationError(RuntimeError):
    """Raised when Supabase is not configured for this local app."""


def get_supabase_client() -> Any:
    """Create a Supabase client from Streamlit secrets without exposing keys."""
    try:
        import streamlit as st
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")
    except Exception as exc:
        raise SupabaseConfigurationError("Supabase configuration could not be loaded.") from exc
    if not url or not key or "your-project" in url or "your-service-role" in key:
        raise SupabaseConfigurationError(
            "Supabase is not configured. Copy .streamlit/secrets.toml.example to secrets.toml and add local credentials."
        )
    return create_client(url, key)
