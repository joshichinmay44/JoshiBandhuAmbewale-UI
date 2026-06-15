import streamlit as st
import requests
from utils.common_util import send_post_request, circular_spinner
import pandas as pd
import time
import math

BACKEND_URL = "http://127.0.0.1:8000"

def get_current_inventory(id = None):
    try:
        if id:
            response = requests.get(f"{BACKEND_URL}/inventory/get_current_inventory/{id}")
        else:
            response = requests.get(f"{BACKEND_URL}/inventory/get_current_inventory")
        if response.status_code == 200:
            response = response.json().get("inventory", [])
            inventory_df= pd.DataFrame(response,columns=[
            "id", "sku_name", "total_units", "Available Stock (in dozens)" ,"unit_cost_price", "total_cost_price", "description", "vendor_name"])
            return inventory_df.rename(columns= {"sku_name": "SKU Name", "total_units": "Total Units", "unit_cost_price": "Unit Cost Price", "total_cost_price": "Total Cost Price", "vendor_name": "Vendor Name"})
        else:
            raise Exception(f"Failed to fetch current inventory: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching current inventory: {e}")


@st.fragment
def current_inventory():
    inventory_df = get_current_inventory()
    selection = st.dataframe(
            inventory_df[["SKU Name", "Available Stock (in dozens)", "Vendor Name"]],
            on_select="rerun",
            selection_mode="single-row",
            selection_default=None,
        )
    
    selected_row = inventory_df.loc[selection.selection.rows] if selection.selection.rows else None
      # Debugging line to check selected rows
    
    if selection.selection.rows:
        st.session_state.inventory_df = selected_row
    else:
        st.session_state.inventory_df = None
    
st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> View Current Inventory </h2>",unsafe_allow_html=True)
data_area = st.empty()

with data_area:
    if "inventory_df" not in st.session_state or st.session_state.inventory_df is None:
        circular_spinner("Please wait...")
        time.sleep(3)  # Simulate loading delay
        current_inventory()