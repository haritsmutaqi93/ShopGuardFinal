import streamlit as st
from backend.ui import configure_page, repository_or_message

configure_page("Dashboard")
repo = repository_or_message()
if repo:
    try:
        summary = repo.dashboard_summary()
        cols = st.columns(3)
        cols[0].metric("Businesses", summary["businesses"])
        cols[1].metric("Successful watermarks", summary["watermarks"])
        cols[2].metric("Verification attempts", summary["verifications"])
        st.subheader("Recent watermark activity")
        records = repo.list_watermarks(10)
        if records:
            st.dataframe(records, use_container_width=True, hide_index=True)
        else:
            st.info("No watermark records yet. Create a business, then embed an image.")
    except Exception:
        st.error("Could not load dashboard data from Supabase. Verify credentials and run the migration.")
