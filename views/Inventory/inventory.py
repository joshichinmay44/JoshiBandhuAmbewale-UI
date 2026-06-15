import streamlit as st
import requests
from utils.common_util import  circular_spinner
import pandas as pd
import time

BACKEND_URL = "http://127.0.0.1:8000"

def get_current_inventory():
    try:
        response = requests.get(f"{BACKEND_URL}/inventory/get_current_inventory")
        if response.status_code == 200:
            response = response.json().get("inventory", [])
            inventory_df= pd.DataFrame(response,columns=[
            "SKU Name", "Vendor Name", "Total Units Received", "Available Stock (in dozens)" , "Available Stock (in units)"])
            return inventory_df.rename(columns= {"sku_name": "SKU Name", "total_units": "Total Units", "unit_cost_price": "Unit Cost Price", "total_cost_price": "Total Cost Price", "vendor_name": "Vendor Name"})
        else:
            raise Exception(f"Failed to fetch current inventory: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching current inventory: {e}")


@st.fragment
def current_inventory():
    inventory_df = get_current_inventory()
    selection = st.dataframe(
            inventory_df,
            hide_index=True
        )
    
st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> View Current Inventory </h2>",unsafe_allow_html=True)
data_area = st.empty()

with data_area:
    if "inventory_df" not in st.session_state or st.session_state.inventory_df is None:
        circular_spinner("Please wait...")
        time.sleep(3)  # Simulate loading delay
        current_inventory()

col1, col2 = st.columns(2)
with st.expander("Choose appropriate action", expanded=True):
    add_customer_button = st.button("Add New SKu", use_container_width=True)
    if add_customer_button:
        st.switch_page("views/Inventory/add_new_sku.py")
    update_customer_button = st.button("View Existing SKUs", use_container_width=True)
    if update_customer_button:
        st.switch_page("views/Inventory/view_sku.py")
    add_inventory_button = st.button("Add Inventory", use_container_width=True)
    if add_inventory_button:
        st.switch_page("views/Inventory/add_inventory.py")