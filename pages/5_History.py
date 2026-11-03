from __future__ import annotations

from datetime import datetime

import streamlit as st

from backend.ui import configure_page, repository_or_message


def display_time(value: str | None) -> str:
    """Present a Supabase UTC timestamp in a readable, timezone-labelled form."""
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d %b %Y, %H:%M UTC")
    except ValueError:
        return value


def watermark_rows(records: list[dict]) -> list[dict]:
    return [
        {
            "Record ID": record.get("id", "—"),
            "Business": (record.get("businesses") or {}).get("business_name") or (record.get("businesses") or {}).get("business_code") or "—",
            "Asset ID": record.get("asset_id", "—"),
            "Original Image": record.get("original_filename", "—"),
            "Watermarked Image": record.get("output_filename", "—"),
            "Status": str(record.get("status", "—")).title(),
            "Created At": display_time(record.get("created_at")),
        }
        for record in records
    ]


def verification_rows(records: list[dict]) -> list[dict]:
    labels = {"valid": "Valid", "not_found": "Not Found", "corrupted": "Corrupted", "error": "Error"}
    return [
        {
            "Verification ID": record.get("id", "—"),
            "Uploaded Image": record.get("uploaded_filename", "—"),
            "Detected Business Code": record.get("detected_business_code") or "—",
            "Detected Asset ID": record.get("detected_asset_id") or "—",
            "Verification Result": labels.get(record.get("result"), str(record.get("result", "—")).title()),
            "Details": record.get("details") or "—",
            "Verified At": display_time(record.get("verified_at")),
        }
        for record in records
    ]


configure_page("ShopGuard Activity History")
st.markdown("<p class='page-subtitle'>Review watermark embedding operations and image verification attempts.</p>", unsafe_allow_html=True)
repo = repository_or_message()
if repo:
    try:
        records = repo.list_watermarks()
        verifications = repo.list_verifications()
        successful = sum(verification.get("result") == "valid" for verification in verifications)
        metrics = st.columns(3)
        metrics[0].metric("Watermark operations", len(records))
        metrics[1].metric("Verification attempts", len(verifications))
        metrics[2].metric("Successful verifications", successful)

        st.subheader("Watermark operations")
        if records:
            st.dataframe(watermark_rows(records), use_container_width=True, hide_index=True, column_config={
                "Record ID": st.column_config.TextColumn(width="small"),
                "Business": st.column_config.TextColumn(width="medium"),
                "Original Image": st.column_config.TextColumn(width="medium"),
                "Watermarked Image": st.column_config.TextColumn(width="medium"),
                "Created At": st.column_config.TextColumn(width="medium"),
            })
        else:
            st.info("No watermark operations have been saved yet.")

        st.subheader("Verification attempts")
        if verifications:
            st.dataframe(verification_rows(verifications), use_container_width=True, hide_index=True, column_config={
                "Verification ID": st.column_config.TextColumn(width="small"),
                "Uploaded Image": st.column_config.TextColumn(width="medium"),
                "Details": st.column_config.TextColumn(width="large"),
                "Verified At": st.column_config.TextColumn(width="medium"),
            })
        else:
            st.info("No verification attempts have been saved yet.")
    except Exception:
        st.error("Could not load history from Supabase. Check credentials, connectivity, and migration setup.")
