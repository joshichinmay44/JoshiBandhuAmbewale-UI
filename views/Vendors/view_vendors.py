import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, City
import time
from utils.common_util import circular_spinner, fetch_zip_codes, send_post_request
import numpy as np

BACKEND_URL = "http://127.0.0.1:8000"


def get_vendors():
    try:
        response = requests.get(f"{BACKEND_URL}/vendor/get_vendors")
        if response.status_code == 200:
            response = response.json().get("vendors", [])
            vendors_df= pd.DataFrame(response,columns=[
            "id", "vendor_name", "contact_name", "email", "phone_number_calling", "phone_number_whatsapp","country", "state", "city", "pincode", "street", "created_at", "updated_at", "created_by", "updated_by"
        ]).sort_values(by="id", ascending=True, ignore_index=True)
            return vendors_df
        else:
            raise Exception(f"Failed to fetch vendors: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching vendors: {e}")
               
@st.fragment
def vendor_selection():
    vendors_df = get_vendors()
    selection = st.dataframe(
            vendors_df,
            on_select="rerun",
            selection_mode="single-row",
            selection_default=None,
        )
    
    if selection.selection.rows:
        st.session_state.vendors_df = vendors_df
        st.switch_page("Views/Vendors/update_vendors.py")

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Select Vendor to edit </h2>",unsafe_allow_html=True)
data_area = st.empty()

with data_area:
    if "vendors_df" not in st.session_state or st.session_state.vendors_df is None:
        circular_spinner("Please wait...")
        time.sleep(3)  # Simulate loading delay
        vendor_selection()