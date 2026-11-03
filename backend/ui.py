"""Small shared helpers for Streamlit pages."""
from __future__ import annotations

import streamlit as st

from database.repository import ShopGuardRepository
from database.supabase_client import SupabaseConfigurationError
from backend.auth import require_authentication


GLOBAL_STYLES = """
<style>
/* A deliberate light palette prevents theme/browser defaults from lowering contrast. */
:root { color-scheme: light; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: #f4f7fb !important;
    color: #172b4d !important;
}
[data-testid="stAppViewContainer"] * { color: #172b4d; }
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background: #ffffff !important;
    color: #172b4d !important;
    border-right: 1px solid #d7e1ee;
}
h1, h2, h3, .stHeading, label, p, li, small, [data-testid="stCaptionContainer"],
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
    color: #172b4d !important;
}
[data-testid="stMetric"], [data-testid="stDataFrame"], [data-testid="stExpander"],
[data-testid="stFileUploader"], [data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border-color: #c9d7e7 !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 2px dashed #5b82aa !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p {
    color: #172b4d !important;
}
[data-testid="stFileUploaderDropzone"] svg {
    fill: #145da0 !important;
    color: #145da0 !important;
    stroke: #145da0 !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: #e7f0fa !important;
    border: 1px solid #145da0 !important;
    color: #0c477e !important;
    font-weight: 700 !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    background: #d4e7f8 !important;
    color: #083863 !important;
}
[data-testid="stMetric"] { border: 1px solid #c9d7e7; border-radius: 10px; padding: 12px; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #102a43 !important; }
input, textarea, [data-baseweb="select"] input, [data-baseweb="select"] div {
    color: #172b4d !important;
    background: #ffffff !important;
}
input::placeholder, textarea::placeholder { color: #52677f !important; opacity: 1 !important; }
[data-baseweb="select"] > div, [data-baseweb="input"] > div {
    background: #ffffff !important;
    border-color: #8ca4bd !important;
}
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
    color: #ffffff !important;
    background: #145da0 !important;
    border: 1px solid #0c477e !important;
    font-weight: 700 !important;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: #0c477e !important;
    color: #ffffff !important;
}
[data-testid="stPageLink-NavLink"] {
    align-items: flex-start !important;
    background: #ffffff !important;
    border: 1px solid #c9d7e7 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 7px rgba(20, 60, 100, 0.08) !important;
    color: #172b4d !important;
    display: flex !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    line-height: 1.5 !important;
    box-sizing: border-box !important;
    height: 142px !important;
    min-height: 142px !important;
    padding: 22px !important;
    white-space: pre-line !important;
}
[data-testid="stPageLink-NavLink"]:hover {
    background: #edf5fc !important;
    border-color: #145da0 !important;
    box-shadow: 0 5px 14px rgba(20, 93, 160, 0.16) !important;
    color: #0c477e !important;
    text-decoration: none !important;
}
.page-subtitle { color: #52677f !important; font-size: 1.06rem; margin: -0.45rem 0 1.2rem; }
.metric-explanation { color: #40566f !important; font-size: 0.92rem; line-height: 1.45; }
.app-footer { color: #52677f !important; font-size: 0.85rem; margin-top: 2.5rem; text-align: center; }
.stButton > button:disabled { background: #9aaabd !important; color: #ffffff !important; opacity: 1 !important; }
[data-testid="stAlert"] { border-width: 1px !important; }
[data-testid="stAlert"] p, [data-testid="stAlert"] div { color: #102a43 !important; font-weight: 500; }
button, [role="button"], a { color: inherit; }
</style>
"""


def configure_page(title: str) -> None:
    st.set_page_config(page_title=f"ShopGuard | {title}", page_icon="🛡️", layout="wide")
    st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)
    require_authentication()
    st.title(f"🛡️ {title}")


def repository_or_message() -> ShopGuardRepository | None:
    try:
        return ShopGuardRepository()
    except SupabaseConfigurationError as exc:
        st.warning(str(exc))
        return None
    except Exception:
        st.error("Supabase connection failed. Check your URL, service-role key, network, and migration setup.")
        return None


def fragile_notice() -> None:
    st.info("LSB watermarks survive an unchanged PNG, but JPEG recompression, resizing, cropping, filters, and screenshots can destroy them. CRC32 detects accidental corruption; it is not cryptographic proof of ownership.")
