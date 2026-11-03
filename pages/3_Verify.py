from __future__ import annotations
import streamlit as st
from backend.image_service import ImageValidationError, load_rgb_image, to_array
from backend.ui import configure_page, fragile_notice, repository_or_message
from watermark.extract import extract_frame

configure_page("Verify watermark")
fragile_notice()
repo = repository_or_message()
uploaded = st.file_uploader("Candidate PNG or JPEG", type=["png", "jpg", "jpeg"])
if st.button("Verify image", type="primary", disabled=not uploaded):
    result_name, details, code, asset, record_id = "error", "", None, None, None
    try:
        image, _ = load_rgb_image(uploaded, int(st.secrets.get("MAX_UPLOAD_MB", 10)))
        result = extract_frame(to_array(image)); result_name, details = result.status, result.details or ""
        if result.payload:
            code, asset = result.payload.business_code, result.payload.asset_id
            st.success("Valid ShopGuard watermark found."); st.json({"business_code": code, "asset_id": asset, "version": result.payload.version})
            if repo:
                try:
                    found = repo.find_watermark_record(code, asset); record_id = found["id"] if found else None
                except Exception: pass
        elif result.status == "not_found": st.info("No ShopGuard watermark was found in this image.")
        else: st.warning(f"Watermark appears corrupted or incomplete: {details}")
    except ImageValidationError as exc:
        details = str(exc); st.error(details)
    if repo:
        try:
            repo.log_verification({"watermark_record_id": record_id, "uploaded_filename": uploaded.name, "detected_business_code": code, "detected_asset_id": asset, "result": result_name, "details": details})
            st.caption("Verification attempt saved to Supabase.")
        except Exception: st.error("Verification result was shown, but its history log could not be saved to Supabase.")
    else: st.warning("Verification result was not logged because Supabase is not configured.")
