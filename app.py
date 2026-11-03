"""ShopGuard Streamlit entry point."""
import streamlit as st
from backend.auth import require_authentication
from backend.ui import GLOBAL_STYLES

st.set_page_config(page_title="ShopGuard", page_icon="🛡️", layout="wide")
st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)
require_authentication()
st.markdown("""
<style>
[data-testid="stMainBlockContainer"] { max-width: 980px; padding-top: 2.5rem; }
.hero { padding: 2rem 2.25rem; background: linear-gradient(120deg, #0b2f55, #1d6eae); border-radius: 16px; margin-bottom: 1.75rem; }
.hero h1, .hero p { color: #ffffff !important; }
.hero h1 { font-size: 2.25rem; margin: 0 0 .45rem; }
.hero p { font-size: 1.08rem; margin: 0; }
/* Homepage-only overrides for a compact, uniform 2 × 2 navigation grid. */
[data-testid="stPageLink-NavLink"] { height: 134px !important; min-height: 134px !important; padding: 17px 18px !important; }
</style>
""", unsafe_allow_html=True)
st.markdown("""<div class='hero'><h1>🛡️ Protect your product images.</h1><p>Invisible digital watermarking for e-commerce image ownership identification.</p></div>""", unsafe_allow_html=True)
st.header("Welcome to ShopGuard")
st.markdown("<p class='page-subtitle'>Choose an operation to get started.</p>", unsafe_allow_html=True)
first, second = st.columns(2, gap="medium")
with first:
    st.page_link("pages/2_Embed.py", label="🖼️  Embed Watermark\n\nInsert an invisible identifier into your product image.")
with second:
    st.page_link("pages/3_Verify.py", label="🔎  Verify Image\n\nExtract and verify an existing ShopGuard watermark.")

third, fourth = st.columns(2, gap="medium")
with third:
    st.page_link("pages/4_Compare.py", label="📊  Compare Images\n\nEvaluate image quality using MSE and PSNR.")
with fourth:
    st.page_link("pages/5_History.py", label="🗂️  Operation History\n\nReview saved watermark and verification records.")
st.markdown("<p class='app-footer'>ShopGuard · Academic Prototype</p>", unsafe_allow_html=True)
