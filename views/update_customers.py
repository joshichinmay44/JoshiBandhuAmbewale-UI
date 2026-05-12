import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, City

countries = Country.get_countries()
country_names = {c.name: c for c in countries}

def get_cities(country: dict, state: dict):
    cities = City.get_cities_of_state(country.iso2,state.iso_code)
    city_names = [c.name for c in cities]
    return city_names

def get_states(country: dict):
    states = State.get_states_of_country(country.iso2)
    state_names = {s.name: s for s in states}
    return state_names

def fetch_zip_codes(city :str):
    try:
        response = requests.get(f"{BACKEND_URL}/address/get_pin_codes/{city}")
        if response.status_code == 200:
            return response.json().get("pin_codes", [])
        else:
            raise Exception(f"Failed to fetch zip codes: {response.text}")
    except Exception as e:
        raise Exception(f"Error occurred while fetching zip codes: {e}")
    

BACKEND_URL = "http://127.0.0.1:8000"

response = requests.get(f"{BACKEND_URL}/customer/get_customers")
if response.status_code == 200:
    customers = response.json()['customers']
    customers_df= pd.DataFrame(customers,columns=[
        "id", "first_name", "last_name", "email", "phone_number_calling", "phone_number_whatsapp", "customer_type", "customer_mode","country", "state", "city", "pincode", "street", "created_at", "updated_at", "created_by", "updated_by"
    ])
st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Update Customer </h2>",unsafe_allow_html=True)
st.write("---")

st.session_state.edited_df = None  # Initialize edited_df in session state to persist across interactions

st.markdown(f"<h3 style='text-align: center; color: #6B1D1D ;'> Select a Customer to Edit </h3>",unsafe_allow_html=True)
selection = st.dataframe(
    customers_df,
    on_select="rerun",
    selection_mode="single-row"
)
selected_rows = selection.selection.rows

if selected_rows:
    selected_idx = selected_rows[0]
    # Extract the single row as a new DataFrame for editing
    row_to_edit = customers_df.iloc[[selected_idx]]
    
    st.markdown(f"<h3 style='text-align: center; color: #6B1D1D ;'> Edit Details for ID: {row_to_edit['id'].values[0]}</h3>",unsafe_allow_html=True)
    
    # Enclose editing and submission inside a Form to control API triggers
    if st.session_state.edited_df is None:  # Only initialize edited_df when the form is first rendered for a selection
        with st.form("edit_form"):
        # Reset edited_df on each new selection to avoid stale data issues
            st.session_state.edited_df = True
            edited_df = st.data_editor(
                row_to_edit,
                column_config={
                     "country" : st.column_config.Selectbox(
                        "Country",
                        options=list(country_names.keys()),
                        default = "India"
                    ),
                     "state" : st.column_config.Selectbox(
                        "State",
                        options= get_states(country_names["India"]).keys(),
                    ),
                     "city" : st.column_config.Selectbox(
                        "City",
                        options=[]
                    )
                } ,
                disabled=["id"], # Prevent the user from tampering with the primary key ID
                hide_index=True,
                key="customer_selection"
            )
            
            submit_button = st.form_submit_button("Send Updates to API")
            
            if submit_button:
                # payload = edited_df.to_dict(orient='records')[0]
                payload = {
                        "first_name": edited_df['first_name'].values[0],
                        "last_name": edited_df['last_name'].values[0],
                        "email": edited_df['email'].values[0],
                        "phone_number_calling": edited_df['phone_number_calling'].values[0],
                        "phone_number_whatsapp": edited_df['phone_number_whatsapp'].values[0],
                        "customer_type": edited_df['customer_type'].values[0],
                        "customer_mode": edited_df['customer_mode'].values[0],
                        "updated_by": st.session_state.get("username", "System"),
                        "cust_id": str(edited_df['id'].values[0])  # Default to "Unknown User" if not set 
                    }
                try:
                        response = requests.post(f"{BACKEND_URL}/customer/update_customer", json=payload)
                        if response.status_code == 200:
                            st.success(f"Customer {edited_df['first_name'].values[0]} {edited_df['last_name'].values[0]} updated successfully!")
                        else:
                            st.error(f"Failed to update customer: {response.text}")
                            raise Exception(f"API Error: {response.text}")
                        st.rerun()
                        del st.session_state["customer_selection"]
            
                except requests.exceptions.RequestException as e:
                        st.error(f"Error occurred: {e}")