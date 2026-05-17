import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, City
import time
from utils.common_util import circular_spinner, fetch_zip_codes, send_post_request
import numpy as np

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
        


# 1. Fetch baseline country data records once globally
all_countries = Country.get_countries()
country_map = {c.name: c.iso2 for c in all_countries}
country_names = sorted(list(country_map.keys()))

# 2. Initialize explicit data storage arrays inside Streamlit's engine
if "current_country" not in st.session_state:
    st.session_state.current_country = "India" if "India" in country_names else country_names[0]
if "current_state" not in st.session_state:
    st.session_state.current_state = None
if "current_city" not in st.session_state:
    st.session_state.current_city =  None

# --- PROCESS LIVE CASCADING LOGIC OUTSIDE FORM RESTRICTIONS ---
# A. Get Active States matching chosen country
active_country_iso = country_map[st.session_state.current_country]
all_states = State.get_states_of_country(active_country_iso)
state_map = {s.name: s.iso_code for s in all_states} if all_states else {}
state_options = sorted(list(state_map.keys()))

# Ensure selected state is valid for the current country list
if st.session_state.current_state not in state_options:
    st.session_state.current_state = state_options[0] if state_options else None

# B. Get Active Cities matching chosen state
city_options = []
if st.session_state.current_state and state_map:
    active_state_iso = state_map[st.session_state.current_state]
    all_cities = City.get_cities_of_state(active_country_iso, active_state_iso)
    city_options = sorted([c.name for c in all_cities]) if all_cities else []

if st.session_state.current_city not in city_options:
    st.session_state.current_city = city_options[0] if city_options else None


st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Update Customer </h2>",unsafe_allow_html=True)
st.write("---")

data_area = st.empty()

st.session_state.edited_df = None  # Initialize edited_df in session state to persist across interactions





with data_area:
    circular_spinner("Loading customers...")
    time.sleep(3)
    
    customers_df = get_customers()
    ROWS_PER_PAGE = 10
    total_rows = len(customers_df)
    max_pages = int(np.ceil(total_rows / ROWS_PER_PAGE))
    if max_pages > 1:
        page_number = st.slider(
            "Select Page", 
            min_value=1, 
            max_value=max_pages, 
            value=1
        )
    else:
        page_number = 1
    start_idx = (page_number - 1) * ROWS_PER_PAGE
    end_idx = start_idx + ROWS_PER_PAGE
    

    # 5. Slice and display the data
    paginated_df = customers_df.iloc[start_idx:end_idx]
    st.markdown(f"<h3 style='text-align: center; color: #6B1D1D ;'> Select a Customer to Edit </h3>",unsafe_allow_html=True)
    selection = st.dataframe(
            customers_df,
            on_select="rerun",
            selection_mode="single-row"
        )
    selected_rows = selection.selection.rows
    customers_df = customers_df[["id", "first_name", "last_name", "email", "phone_number_calling", "phone_number_whatsapp", "customer_type", "customer_mode"]]
if selected_rows:
    selected_idx = selected_rows[0]
    # Extract the single row as a new DataFrame for editing
    row_to_edit = customers_df.iloc[[selected_idx]]
    
    st.markdown(f"<h3 style='text-align: center; color: #6B1D1D ;'> Edit Details for customer: {row_to_edit['first_name'].values[0]} {row_to_edit['last_name'].values[0]}</h3>",unsafe_allow_html=True)
    
    # Enclose editing and submission inside a Form to control API triggers
    if st.session_state.edited_df is None:
        with st.container(key="storm_box"):
            update_address = st.radio("Do you want to update the address details?", ["Yes", "No"], index = 1, key="update_address", horizontal=True)
            if update_address == "Yes":
                # Reset edited_df on each new selection to avoid stale data issues
                st.session_state.edited_df = True
                edited_df = st.data_editor(
                    row_to_edit,
                    disabled=["id"], # Prevent the user from tampering with the primary key ID
                    hide_index=True,
                    key="customer_selection"
                )

                # 1. Country Selector Dropdown
                chosen_country = st.selectbox(
                    "Select Country",
                    options=country_names,
                    index=country_names.index(st.session_state.current_country),
                    key="ui_country_node"
                )
                # Check for direct update
                if chosen_country != st.session_state.current_country:
                    st.session_state.current_country = chosen_country
                    st.session_state.current_state = None  # Force child reset
                    st.session_state.current_city = None
                    st.rerun()

                # 2. State Selector Dropdown
                state_index = state_options.index(st.session_state.current_state) if st.session_state.current_state else 0
                chosen_state = st.selectbox(
                    "Select State",
                    options=state_options,
                    index=state_index,
                    disabled=not state_options,
                    key="ui_state_node",
                    placeholder=st.session_state.current_state
                )
                # Check for direct update
                if chosen_state != st.session_state.current_state:
                    st.session_state.current_state = chosen_state
                    st.session_state.current_city = None  # Force child reset
                    st.rerun()

                # 3. City Selector Dropdown
                city_index = city_options.index(st.session_state.current_city) if st.session_state.current_city else 0
                chosen_city = st.selectbox(
                    "Select City",
                    options=city_options,
                    index=city_index,
                    disabled=not city_options,
                    key="ui_city_node",
                )
                if chosen_city != st.session_state.current_city:
                    st.session_state.current_city = chosen_city

                postal_code = st.selectbox("Postal Code / ZIP",options=fetch_zip_codes(st.session_state.current_city), placeholder="444601")
                street = st.text_input("Street Address", key="street_input")
                
                # Update the edited_df with the new address details
                edited_df['country'] = chosen_country
                edited_df['state'] = chosen_state
                edited_df['city'] = chosen_city
                edited_df['pincode'] = postal_code
                edited_df['street'] = street

                submit_button = st.button("Update Customer")
                
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
                            "cust_id": str(edited_df['id'].values[0]),
                            "country": edited_df['country'].values[0],
                            "state": edited_df['state'].values[0],
                            "city": edited_df['city'].values[0],
                            "pincode": str(edited_df['pincode'].values[0]),
                            "street": edited_df['street'].values[0]
                        }
                    res = send_post_request('/customer/update_customer',payload)
                    if res == 200:
                        time.sleep(1)
                        st.rerun()
                    else :
                        st.error ("Could not update customer")
            else:
                st.session_state.edited_df = True
                edited_df = st.data_editor(
                    row_to_edit,
                    disabled=["id"], # Prevent the user from tampering with the primary key ID
                    hide_index=True,
                    key="customer_selection"
                )
                submit_button = st.button("Update Customer")
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
                            "cust_id": str(edited_df['id'].values[0]),
                            "country": None,
                            "state": None, 
                            "city": None,
                            "pincode": None,
                            "street": None
                    }
                    res = send_post_request('/customer/update_customer',payload)
                    if res == 200:
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Could not update customer")
                            
        