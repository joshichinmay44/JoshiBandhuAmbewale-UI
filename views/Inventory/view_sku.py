import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, City
import time
from utils.common_util import circular_spinner, fetch_zip_codes, send_post_request
import numpy as np

BACKEND_URL = "http://127.0.0.1:8000"


def get_sku():
    try:
        response = requests.get(f"{BACKEND_URL}/sku/get_skus")
        if response.status_code == 200:
            response = response.json().get("vendors", [])
            sku_df= pd.DataFrame(response,columns=[
            "id", "sku_name", "description", "created_at", "updated_at", "created_by", "updated_by"])
            return sku_df
        else:
            raise Exception(f"Failed to fetch vendors: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching vendors: {e}")

@st.fragment
def sku_selection():
    sku_df = get_sku()
    selection = st.dataframe(
            sku_df,
            on_select="rerun",
            selection_mode="single-row",
            selection_default=None,
        )
    
    if selection.selection.rows:
        st.session_state.sku_df = sku_df
        st.switch_page("Views/Inventory/update_sku.py")

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Select SKU to edit </h2>",unsafe_allow_html=True)
data_area = st.empty()

with data_area:
    if "sku_df" not in st.session_state or st.session_state.sku_df is None:
        circular_spinner("Please wait...")
        time.sleep(3)  # Simulate loading delay
        sku_selection()