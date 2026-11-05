"""Small shared helpers for Streamlit pages."""
from __future__ import annotations

import streamlit as st

from database.repository import ShopGuardRepository
from database.supabase_client import SupabaseConfigurationError
from backend.auth import require_authentication


GLOBAL_STYLES = """
<style>
/* Keep Streamlit's controls in a predictable, high-contrast light palette. */
:root { color-scheme: light; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: #f4f7fb !important;
    color: #172b4d !important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background: #ffffff !important;
    color: #172b4d !important;
    border-right: 1px solid #d7e1ee;
}
h1, h2, h3, .stHeading, label, p, li, small, [data-testid="stCaptionContainer"],
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
    color: #172b4d !important;
}
[data-testid="stWidgetLabel"] p, label {
    font-weight: 600 !important;
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
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploader"] button {
    background: #e7f0fa !important;
    border: 1px solid #145da0 !important;
    color: #0c477e !important;
    font-weight: 700 !important;
}
[data-testid="stFileUploaderDropzone"] button:hover,
[data-testid="stFileUploader"] button:hover {
    background: #d4e7f8 !important;
    color: #083863 !important;
}
[data-testid="stMetric"] { border: 1px solid #c9d7e7; border-radius: 10px; padding: 12px; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #102a43 !important; }
/* Text fields: never inherit the application background or page text colour. */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="input"] input {
    color: #172b4d !important;
    background: #ffffff !important;
    caret-color: #145da0 !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder,
[data-baseweb="input"] input::placeholder {
    color: #52677f !important;
    opacity: 1 !important;
}
[data-testid="stTextInput"] [data-baseweb="input"] > div,
[data-testid="stTextArea"] [data-baseweb="textarea"],
[data-baseweb="select"] > div {
    background: #ffffff !important;
    border-color: #7893ae !important;
}
[data-testid="stTextInput"] [data-baseweb="input"] > div:focus-within,
[data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: #145da0 !important;
    box-shadow: 0 0 0 2px rgba(20, 93, 160, 0.22) !important;
}
/* Select options render in a BaseWeb popover outside the closed select's DOM. */
[data-baseweb="popover"],
[role="listbox"] {
    background: #ffffff !important;
    color: #172b4d !important;
    border: 1px solid #7893ae !important;
    box-shadow: 0 6px 18px rgba(20, 60, 100, 0.18) !important;
}
[role="option"],
[role="listbox"] li,
[data-baseweb="menu"] [role="option"] {
    background: #ffffff !important;
    color: #172b4d !important;
}
[role="option"] *,
[role="listbox"] li *,
[data-baseweb="menu"] [role="option"] * {
    color: #172b4d !important;
}
[role="option"]:hover,
[role="option"][aria-selected="true"],
[role="option"][aria-selected="true"] *,
[role="option"][data-highlighted="true"],
[role="option"][data-highlighted="true"] * {
    background: #e7f0fa !important;
    color: #0c477e !important;
}
[data-baseweb="select"] input {
    color: #172b4d !important;
}
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
    color: #ffffff !important;
    background: #145da0 !important;
    border: 1px solid #0c477e !important;
    font-weight: 700 !important;
}
.stButton > button *, .stDownloadButton > button *, [data-testid="stFormSubmitButton"] > button * {
    color: #ffffff !important;
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
[data-testid="stAlert"][data-baseweb="notification"][kind="positive"] { background: #e8f5ed !important; }
[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] { background: #fff7e5 !important; }
[data-testid="stAlert"][data-baseweb="notification"][kind="negative"] { background: #fdecec !important; }
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
