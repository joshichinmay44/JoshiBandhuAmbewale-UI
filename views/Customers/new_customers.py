import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, City
from utils.common_util import fetch_zip_codes, send_post_request,  circular_spinner

BACKEND_URL = "http://127.0.0.1:8000"


dataarea = st.empty()

all_countries = Country.get_countries()
country_map = {c.name: c.iso2 for c in all_countries}
country_names = sorted(list(country_map.keys()))

# 2. Initialize explicit data storage arrays inside Streamlit's engine
if "current_new_customer_country" not in st.session_state:
    st.session_state.current_new_customer_country = "India" if "India" in country_names else country_names[0]
if "current_new_customer_state" not in st.session_state:
    st.session_state.current_new_customer_state = None
if "current_new_customer_city" not in st.session_state:
    st.session_state.current_new_customer_city = None

# --- PROCESS LIVE CASCADING LOGIC OUTSIDE FORM RESTRICTIONS ---
# A. Get Active States matching chosen country
active_country_iso = country_map[st.session_state.current_country]
all_states = State.get_states_of_country(active_country_iso)
state_map = {s.name: s.iso_code for s in all_states} if all_states else {}
state_options = sorted(list(state_map.keys()))

# Ensure selected state is valid for the current country list
if st.session_state.current_new_customer_state not in state_options:
    st.session_state.current_new_customer_state = state_options[0] if state_options else None

# B. Get Active Cities matching chosen state
city_options = []
if st.session_state.current_new_customer_state and state_map:
    active_state_iso = state_map[st.session_state.current_new_customer_state]
    all_cities = City.get_cities_of_state(active_country_iso, active_state_iso)
    city_options = sorted([c.name for c in all_cities]) if all_cities else []

if st.session_state.current_new_customer_city not in city_options:
    st.session_state.current_new_customer_city = city_options[0] if city_options else None

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
        st.session_state.current_new_customer_state = None  # Force child reset
        st.session_state.current_new_customer_city = None
        st.rerun()

    # 2. State Selector Dropdown
    state_index = state_options.index(st.session_state.current_new_customer_state) if st.session_state.current_new_customer_state else 0
    chosen_state = st.selectbox(
        "Select State",
        options=state_options,
        index=state_index,
        disabled=not state_options,
        key="ui_state_node"
    )
    # Check for direct update
    if chosen_state != st.session_state.current_new_customer_state:
        st.session_state.current_new_customer_state = chosen_state
        st.session_state.current_new_customer_city = None  # Force child reset
        st.rerun()

    # 3. City Selector Dropdown
    city_index = city_options.index(st.session_state.current_new_customer_city) if st.session_state.current_new_customer_city else 0
    chosen_city = st.selectbox(
        "Select City",
        options=city_options,
        index=city_index,
        disabled=not city_options,
        key="ui_city_node"
    )
    if chosen_city != st.session_state.current_new_customer_city:
        st.session_state.current_new_customer_city = chosen_city

    # Additional standard form input elements inside the canvas bounding block
    postal_code = st.selectbox("Postal Code / ZIP",options=fetch_zip_codes(st.session_state.current_new_customer_city), placeholder="444601")
    street = st.text_input("Street Address", key="street_input")
    # Custom form submit action button
    if st.button("Save Form Profile", type="primary"):
        if chosen_country and chosen_state and chosen_city:
            payload = {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "phone_number_calling": phone_number_calling,
                            "phone_number_whatsapp": phone_number_whatsapp,
                            "customer_type":customer_type,
                            "customer_mode": customer_mode,
                            "created_by": st.session_state.get("username", "System"),
                            "country": chosen_country,
                            "state": chosen_state,
                            "city": chosen_state,
                            "pincode": str(postal_code),
                            "street": street,
                        }
            res = send_post_request('customer/add_customer',payload)
            if res == 200:
                st.success("Customer added succefully")
            else:
                st.error("Error adding customer")
        else:
            st.error("Please complete all location fields before submitting.")
    if st.button("View/Update Customers", type="primary"):
        st.switch_page("views/Customers/update_customers.py")
