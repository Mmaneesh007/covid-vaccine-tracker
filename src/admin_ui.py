"""
Admin UI for API Key Management (Developer Portal).
"""
import streamlit as st
import pandas as pd
from src.auth import create_api_key, get_all_keys

def render_admin_panel():
    """Render the Developer Portal in the main area."""
    st.title("🔑 Developer Portal")
    st.markdown("Manage API keys for the COVID-19 Vaccine Tracker API.")
    
    tab1, tab2 = st.tabs(["Generate Key", "Active Keys"])
    
    with tab1:
        st.subheader("Generate New API Key")
        
        with st.form("generate_key_form"):
            owner_name = st.text_input("Client / Developer Name", placeholder="e.g., University Research Lab")
            tier = st.selectbox("Usage Tier", ["free", "pro", "enterprise"])
            
            submitted = st.form_submit_button("Generate Key")
            
            if submitted:
                if not owner_name:
                    st.error("Please enter an owner name.")
                else:
                    new_key = create_api_key(owner_name, tier)
                    if new_key:
                        st.success("API Key Generated Successfully!")
                        st.warning("⚠️ Copy this key now. You won't be able to see it again!")
                        st.code(new_key, language="text")
                        st.balloons()
                    else:
                        st.error("Failed to generate key. Check logs.")
    
    with tab2:
        st.subheader("Active API Keys")
        try:
            df = get_all_keys()
            if not df.empty:
                # Mask the key hash for security (it's already hashed but let's be clean)
                # Actually we don't show the key at all, just metadata
                st.dataframe(
                    df,
                    column_config={
                        "created_at": st.column_config.DatetimeColumn("Created At", format="D MMM YYYY, h:mm a"),
                        "is_active": st.column_config.CheckboxColumn("Active"),
                    },
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No API keys found.")
        except Exception as e:
            st.error(f"Error fetching keys: {e}")
