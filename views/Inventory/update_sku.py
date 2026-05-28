import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, City
import time
from utils.common_util import circular_spinner, fetch_zip_codes, send_post_request
import numpy as np

BACKEND_URL = "http://127.0.0.1:8000"
        
sku_df = st.session_state.get("sku_df", None)

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Update Customer </h2>",unsafe_allow_html=True)
st.write("---")

if sku_df is not None:
    # Extract the single row as a new DataFrame for editing    
    st.markdown(f"<h3 style='text-align: center; color: #6B1D1D ;'> Edit Details for SKU: {sku_df['sku_name'].values[0]}</h3>",unsafe_allow_html=True)
    st.session_state.edited_df = None
    # Enclose editing and submission inside a Form to control API triggers
    if st.session_state.edited_df is None:
        with st.container(key="storm_box"):
            edited_df = st.data_editor(
                sku_df,
                disabled=["id"], # Prevent the user from tampering with the primary key ID
                hide_index=True,
                key="customer_selection"
            )
            st.session_state.edited_df = edited_df
            if st.button("Submit Updated SKU Details", type="primary"):
                payload = {
                    "sku_id": str(st.session_state.edited_df['id'].values[0]),
                    "sku_name": st.session_state.edited_df['sku_name'].values[0],
                    "description": st.session_state.edited_df['description'].values[0],
                    "updated_by": st.session_state.username
                }
                res = send_post_request('sku/update_sku',payload)
                if res == 200:
                    st.success("SKU details updated successfully")
                    time.sleep(3)
                    st.session_state.sku_df = None  # Clear the session state to force a fresh fetch on next view
                    st.switch_page("views/Inventory/view_sku.py")
                else:
                    st.error(f"Failed to update SKU details. Please try again. Error: {res}")
