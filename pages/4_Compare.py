import math

import streamlit as st

from backend.evaluation import mse_and_psnr
from backend.image_service import ImageValidationError, load_rgb_image, to_array
from backend.ui import configure_page


configure_page("Image Quality Comparison")
st.markdown("<p class='page-subtitle'>Evaluate the visual impact of invisible watermark embedding.</p>", unsafe_allow_html=True)

left, right = st.columns(2)
with left:
    original_upload = st.file_uploader("Original image", type=["png", "jpg", "jpeg"], key="original")
with right:
    output_upload = st.file_uploader("Watermarked or candidate image", type=["png", "jpg", "jpeg"], key="output")

if original_upload and output_upload:
    try:
        original, _ = load_rgb_image(original_upload, int(st.secrets.get("MAX_UPLOAD_MB", 10)))
        output, _ = load_rgb_image(output_upload, int(st.secrets.get("MAX_UPLOAD_MB", 10)))
        preview_left, preview_right = st.columns(2)
        with preview_left:
            st.image(original, caption="Original", width=400)
        with preview_right:
            st.image(output, caption="Watermarked / candidate", width=400)

        mse, psnr = mse_and_psnr(to_array(original), to_array(output))
        metric_left, metric_right = st.columns(2)
        with metric_left:
            st.metric("MSE", f"{mse:.6f}")
            st.markdown("<p class='metric-explanation'><strong>MSE (Mean Squared Error):</strong> Measures the average squared pixel difference between two images. Lower values indicate greater similarity.</p>", unsafe_allow_html=True)
        with metric_right:
            st.metric("PSNR", "∞ dB" if math.isinf(psnr) else f"{psnr:.2f} dB")
            st.markdown("<p class='metric-explanation'><strong>PSNR (Peak Signal-to-Noise Ratio):</strong> Measures image quality relative to the original. Higher values generally indicate less visible distortion.</p>", unsafe_allow_html=True)

        if mse == 0:
            st.info("The compared RGB pixel arrays are identical. This result does not establish that the files have the same provenance.")
        else:
            st.info("Metrics are calculated from the uploaded RGB pixel arrays at their original dimensions.")
    except ImageValidationError as exc:
        st.error(str(exc))
    except ValueError:
        st.warning("Metrics cannot be calculated: images have different dimensions. ShopGuard will not resize them.")
else:
    st.info("Upload both images to display side-by-side previews and quality metrics.")
