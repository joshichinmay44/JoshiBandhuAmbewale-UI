import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, City

BACKEND_URL = "http://127.0.0.1:8000"

def fetch_zip_codes(city :str):
    try:
        response = requests.get(f"{BACKEND_URL}/address/get_pin_codes/{city}")
        if response.status_code == 200:
            return response.json().get("pin_codes", [])
        else:
            raise Exception(f"Failed to fetch zip codes: {response.text}")

    except Exception as e:
        raise Exception(f"Error occurred while fetching zip codes: {e}")
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
    st.session_state.current_city = None

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

with st.container(key="storm_box"):
    st.write("### New Customer Details")
    first_name = st.text_input("first_name", placeholder="e.g. admin")
    last_name = st.text_input("last_name", placeholder="eg. admin")
    email = st.text_input("email", placeholder="e.g. admin@example.com")
    phone_number_calling = st.text_input("phone_number_calling", placeholder="e.g. 123-456-7890")
    phone_number_whatsapp = st.text_input("phone_number_whatsapp", placeholder="e.g. 123-456-7890")
    customer_type = st.selectbox("customer_type", ["Retail", "Wholesale"])
    customer_mode = st.selectbox("customer_mode", ["Online", "Offline"])
    created_by = st.session_state.get("username", "System")  
    st.text("Address Details")
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
        key="ui_state_node"
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
        key="ui_city_node"
    )
    if chosen_city != st.session_state.current_city:
        st.session_state.current_city = chosen_city

    # Additional standard form input elements inside the canvas bounding block
    postal_code = st.selectbox("Postal Code / ZIP",options=fetch_zip_codes(st.session_state.current_city), placeholder="444601")
    
    # Custom form submit action button
    if st.button("Save Form Profile", type="primary"):
        if chosen_country and chosen_state and chosen_city:
            st.success(f"Form Saved: {chosen_city}, {chosen_state}, {chosen_country} | Postal Code: {postal_code}")
        else:
            st.error("Please complete all location fields before submitting.")
    if st.button("View/Update Customers", type="primary"):
        st.switch_page("views/update_customers.py")
