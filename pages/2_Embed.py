from __future__ import annotations
import streamlit as st
from PIL import Image
from backend.evaluation import mse_and_psnr
from backend.image_service import ImageValidationError, image_to_png_bytes, load_rgb_image, to_array
from backend.ui import configure_page, fragile_notice, repository_or_message
from watermark.embed import CapacityError, capacity_bits, embed_frame
from watermark.payload import build_frame

configure_page("Embed watermark")
fragile_notice()
repo = repository_or_message()
businesses = []
if repo:
    try: businesses = repo.list_businesses()
    except Exception: st.error("Could not load businesses from Supabase.")

with st.expander("Create business profile"):
    with st.form("business_form", clear_on_submit=True):
        code = st.text_input("Business code", placeholder="FH-001")
        name = st.text_input("Business name", placeholder="Fresh Harvest")
        if st.form_submit_button("Create business"):
            if not repo: st.error("Configure Supabase before creating a business.")
            elif not code.strip() or not name.strip(): st.error("Business code and name are required.")
            else:
                try: repo.create_business(code, name); st.success("Business created. Refresh or rerun to select it.")
                except Exception: st.error("Business could not be saved. Codes must be unique; check Supabase connectivity.")

if not businesses:
    st.info("Create a business profile above before embedding. Supabase is required to persist profiles and operation history.")

lookup = {f"{b['business_code']} — {b['business_name']}": b for b in businesses}
selected_label = st.selectbox("Business profile", list(lookup), disabled=not businesses, placeholder="Select a business")
uploaded = st.file_uploader("Product image (PNG or JPEG)", type=["png", "jpg", "jpeg"])
asset_id = st.text_input("Asset ID", placeholder="IMG-0001", help="Use an identifier unique to this business, such as IMG-0001.")

if uploaded:
    try:
        original, _ = load_rgb_image(uploaded, int(st.secrets.get("MAX_UPLOAD_MB", 10)))
        frame = build_frame(lookup[selected_label]["business_code"], asset_id) if asset_id.strip() and selected_label else None
        info_column, preview_column = st.columns([3, 2], vertical_alignment="center")
        with info_column:
            st.caption(f"Image capacity: {capacity_bits(to_array(original))} bits" + (f" · Required: {len(frame)*8} bits" if frame else " · Enter an asset ID to calculate required capacity."))
            st.caption(f"Image dimensions: {original.width} × {original.height} pixels")
        with preview_column:
            st.image(original, caption="Original upload preview", width=400)
    except (ImageValidationError, ValueError) as exc:
        st.error(str(exc))

st.divider()
st.subheader("Generate protected PNG")
st.caption("Select a business, upload a product image, and enter an asset ID. Then generate the lossless watermarked PNG.")
if st.button("Embed watermark and generate PNG", type="primary", use_container_width=True):
    if not businesses or not selected_label:
        st.error("Select or create a business profile before embedding.")
    elif not uploaded:
        st.error("Upload a PNG or JPEG product image before embedding.")
    elif not asset_id.strip():
        st.error("Enter an asset ID before embedding.")
    else:
        try:
            original, _ = load_rgb_image(uploaded, int(st.secrets.get("MAX_UPLOAD_MB", 10)))
            business = lookup[selected_label]
            frame = build_frame(business["business_code"], asset_id)
            watermarked_array = embed_frame(to_array(original), frame)
            output = Image.fromarray(watermarked_array, "RGB")
            png_bytes = image_to_png_bytes(output)
            mse, psnr = mse_and_psnr(to_array(original), watermarked_array)
            filename = f"{asset_id.strip()}_shopguard.png"
            st.session_state["compare_original"] = original
            st.session_state["compare_output"] = output
            cols = st.columns(2)
            cols[0].image(original, caption="Original", width=400)
            cols[1].image(output, caption="Watermarked PNG", width=400)
            st.metric("MSE", f"{mse:.6f}"); st.metric("PSNR", "∞ dB" if psnr == float("inf") else f"{psnr:.2f} dB")
            st.download_button("Download watermarked PNG", png_bytes, filename, "image/png")
            values = {"business_id": business["id"], "asset_id": asset_id.strip(), "original_filename": uploaded.name, "output_filename": filename, "status": "embedded"}
            try:
                record = repo.create_watermark_record(values) if repo else None
                if record: st.success("Watermark generated and operation metadata saved to Supabase.")
                else: st.warning("Watermark generated, but no Supabase record was saved because configuration is unavailable.")
            except Exception:
                st.warning("Watermark generated, but its history record was not saved. Check Supabase (asset IDs must be unique per business).")
        except (ImageValidationError, CapacityError, ValueError) as exc:
            st.error(str(exc))
