import streamlit as st
import pandas as pd
from country_state_city import Country, State, City
import time
import requests
from utils.common_util import circular_spinner, fetch_zip_codes, send_post_request, get_customers_list, get_sku_list

BACKEND_URL = "http://127.0.0.1:8000"




@st.fragment
def new_booking_form():
    with st.container(key="storm_box"):
        customers_list = get_customers_list()
        sku_list = get_sku_list()
        if customers_list is None:
            st.warning("No customers found. Please add a customer before creating a booking.")   
        if sku_list is None:
            st.warning("No SKUs found. Please add a SKU before creating a booking.") 
        customer_name = st.selectbox("Select Customer", options= customers_list)
        sku_name = st.selectbox("Select SKU", options= sku_list)
        quantity = st.number_input("Quantity (in dozen)", min_value=1.0, step=0.25)
        # Additional booking details can be added here (e.g., booking date, service type, etc.)
        
        if st.button("Create Booking"):
            # Logic to create a new booking can be implemented here
            payload = {
                "customer_name": customer_name,
                "sku_name": sku_name,
                "quantity": str(quantity),
                "lead_generated_by": st.session_state.username,
                "created_by": st.session_state.username
            }

            if not customer_name or not sku_name or not quantity:
                st.error("Please fill in all the required fields.")
                return
            response = send_post_request(f"/sales/add_booking", payload)
            if response == 200:
                st.success(f"Booking created for {customer_name}!")
            else:
                st.error(f"Failed to create booking. {response}")

data_area = st.empty()

with data_area:
    circular_spinner("Please wait...")
    time.sleep(6)  # Simulate loading delay
    new_booking_form()


