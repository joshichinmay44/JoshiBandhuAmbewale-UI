import streamlit as st
import requests
import pandas as pd
import time
from utils.common_util import circular_spinner, fetch_zip_codes, send_post_request
import numpy as np

BACKEND_URL = "http://127.0.0.1:8000"

def get_bookings():
    try:
        response = requests.get(f"{BACKEND_URL}/sales/get_bookings")
        if response.status_code == 200:
            response = response.json().get("bookings", [])
            bookings_df = pd.DataFrame(response,columns=[
            "booking_id", "customer_name", "sku_name","sku_units","booked_quantity_in_doz" ,"delivery_mode","delivery_address", "customer_phone_number_calling", "customer_phone_number_whatsapp", "customer_type","sale_booked_by","booking_date"]).sort_values(by="booking_id", ascending=True, ignore_index=True)
            return bookings_df
        else:
            raise Exception(f"Failed to fetch bookings: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching bookings: {e}")

@st.fragment
def sku_selection():
    bookings_df = get_bookings()
    selection = st.dataframe(
            bookings_df,
            on_select="rerun",
            selection_mode="single-row",
            selection_default=None,
        )
    
    selected_row = bookings_df.loc[selection.selection.rows] if selection.selection.rows else None
    
    if selection.selection.rows:
        st.session_state.bookings_df = selected_row
    #     st.switch_page("Views/Inventory/update_sku.py")

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Select SKU to edit </h2>",unsafe_allow_html=True)
data_area = st.empty()

with data_area:
    if "bookings_df" not in st.session_state or st.session_state.bookings_df is None:
        circular_spinner("Please wait...")
        time.sleep(8)  # Simulate loading delay
        sku_selection()