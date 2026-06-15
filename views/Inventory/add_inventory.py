import streamlit as st
import requests
from utils.common_util import send_post_request, circular_spinner
import pandas as pd
import time
import math

BACKEND_URL = "http://127.0.0.1:8000"

def get_sku_names():
    try:
        response = requests.get(f"{BACKEND_URL}/sku/get_skus")
        if response.status_code == 200:
            response = response.json().get("skus", [])
            sku_df= pd.DataFrame(response,columns=[
            "id", "sku_name", "description", "created_at", "updated_at", "created_by", "updated_by"])
            sku_names =[row["sku_name"] for index, row in sku_df.iterrows()]
            return sku_names
        else:
            raise Exception(f"Failed to fetch vendors: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching vendors: {e}")

def get_vendor_names():
    try:
        response = requests.get(f"{BACKEND_URL}/vendor/get_vendors")
        if response.status_code == 200:
            response = response.json().get("vendors", [])
            vendors_df= pd.DataFrame(response,columns=[
            "id", "vendor_name", "contact_name", "email", "phone_number_calling", "phone_number_whatsapp","country", "state", "city", "pincode", "street", "created_at", "updated_at", "created_by", "updated_by"])
            vendor_names =[row["vendor_name"] for index, row in vendors_df.iterrows()]
            return vendor_names
        else:
            raise Exception(f"Failed to fetch vendors: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching vendors: {e}")

@st.fragment
def add_inventory_form():
    with st.container(key="storm_box"):
        st.write("### Add Inventory")
        sku = st.selectbox("Select SKU", options = sku_names, index = 0, key ='ui_select_sku')
        total_units = st.number_input("Total Units", min_value=1, step=1, key='ui_total_units')
        unit_price = st.number_input("Unit Price", min_value=0.01, step=0.01, key='ui_unit_price')
        total_price = total_units * unit_price
        additional_comments = st.text_input("Additional Comments", placeholder="eg. 30 mangoes packed in a box were great")
        vendor = st.selectbox("Select Vendor", options = vendor_names, index = 0, key='ui_select_vendor')
        if st.button("Add to basket", type="primary"):
            st.session_state.inventory_details.append({
                "sku_name": sku,
                "total_units": total_units,
                "unit_cost_price": unit_price,
                "total_cost_price": total_price,
                "description": additional_comments,
                "vendor_name": vendor,
                "created_by": st.session_state.username
            })
            st.success("Inventory details saved successfully!")
        else:
            if not sku or not unit_price or not total_units or not vendor:
                st.error("Please complete all location fields before submitting.")

        inventory_df = pd.DataFrame(st.session_state.inventory_details, columns=["sku_name", "total_units", "unit_cost_price", "total_cost_price", "description", "vendor_name", "created_by"])
        st.write("### Inventory Basket")
        edited_df = st.data_editor(
                inventory_df,
                disabled=["sku_name","vendor_name","total_cost_price"],  # Prevent the user from tampering with the primary key ID
                hide_index=False,
                num_rows="dynamic",
                key="customer_selection"
            )
        if not edited_df.equals(inventory_df):
            clean_array = [
                {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in row.items()}
                for row in edited_df.to_dict('records')
            ]
            
            for row in clean_array:
                row["total_cost_price"] = row["total_units"] * row["unit_cost_price"] if row["total_units"] is not None and row["unit_cost_price"] is not None else 0
            
            st.session_state.inventory_details = clean_array
              # Update session state with edited details
        if st.button("Save batch", type="primary"):
            payload = st.session_state.inventory_details
            if len(payload) == 0:
                st.error("No inventory details to save. Please add items to the basket before saving.")
                return
            res = send_post_request('inventory/add_inventory',payload)
            if res == 200:
                st.session_state.inventory_details = []  # Clear the inventory details after successful submission
                st.success("Inventory batch added successfully!")
                time.sleep(3)  # Pause briefly to show success message
                st.switch_page("views/Inventory/inventory.py")  # Redirect to inventory view page after saving
            else:
                st.error(f"Failed to add inventory batch. Please try again. Error: {res}")
        

data_area = st.empty()
with data_area:
    circular_spinner("Please wait...")
    time.sleep(3)  # Simulate loading delay
    sku_names = get_sku_names()
    vendor_names = get_vendor_names()
    add_inventory_form()
    # more_items = st.radio("Do you want to add more items?", options=["Yes", "No"], index = 1, key="inventory_view_radio")

    # if more_items == "Yes":
    #     st.switch_page("views/Inventory/add_inventory.py")  # Rerun the app to show the form again
    # else:
    #     st.write(st.session_state.inventory_details)  # Display the list of inventory details added in this session
    