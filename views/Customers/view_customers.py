import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, City
import time
from utils.common_util import circular_spinner

BACKEND_URL = "http://127.0.0.1:8000"



def get_customers():
    try:
        response = requests.get(f"{BACKEND_URL}/customer/get_customers")
        if response.status_code == 200:
            response = response.json().get("customers", [])
            customers_df= pd.DataFrame(response,columns=[
            "id", "first_name", "last_name", "email", "phone_number_calling", "phone_number_whatsapp", "customer_type", "customer_mode","country", "state", "city", "pincode", "street", "created_at", "updated_at", "created_by", "updated_by"
        ])
            return customers_df
        else:
            raise Exception(f"Failed to fetch customers: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching customers: {e}")
        
@st.fragment
def customer_selection():
    customers_df = get_customers()
    selection = st.dataframe(
            customers_df,
            on_select="rerun",
            selection_mode="single-row",
            selection_default=None,
        )
    selected_row = customers_df.loc[selection.selection.rows] if selection.selection.rows else None
      # Debugging line to check selected rows
    
    if selection.selection.rows:
        st.session_state.customers_df = selected_row
        st.switch_page("Views/Customers/update_customers.py")

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Select Customer to edit </h2>",unsafe_allow_html=True)
data_area = st.empty()

with data_area:
    if "customers_df" not in st.session_state or st.session_state.customers_df is None:
        circular_spinner("Please wait...")
        time.sleep(3)  # Simulate loading delay
        customer_selection()