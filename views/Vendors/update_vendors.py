import streamlit as st
import requests
import pandas as pd
from country_state_city import Country, State, Citycity
import time
from utils.common_util import circular_spinner, fetch_zip_codes, send_post_request


vendors_df = st.session_state.get("vendors_df", None)


# 1. Fetch baseline country data records once globally
all_countries = Country.get_countries()
country_map = {c.name: c.iso2 for c in all_countries}
country_names = sorted(list(country_map.keys()))
# 2. Initialize explicit data storage arrays inside Streamlit's engine
if "current_update_vendor_country" not in st.session_state:
    st.session_state.current_update_vendor_country = vendors_df['country'].values[0] if vendors_df is not None and not vendors_df['country'].isna().all() else 'India'
if "current_update_vendor_state" not in st.session_state:
    st.session_state.current_update_vendor_state = vendors_df['state'].values[0] if vendors_df is not None and not vendors_df['state'].isna().all() else 'Maharashtra'
if "current_update_vendor_city" not in st.session_state:
    st.session_state.current_update_vendor_city =  vendors_df['city'].values[0] if vendors_df is not None and not vendors_df['city'].isna().all() else 'Pune'
if 'current_update_vendor_pincode' not in st.session_state:
    st.session_state.current_update_vendor_pincode = vendors_df['pincode'].values[0] if vendors_df is not None and not vendors_df['pincode'].isna().all() else '415605'

# --- PROCESS LIVE CASCADING LOGIC OUTSIDE FORM RESTRICTIONS ---
# A. Get Active States matching chosen country
active_country_iso = country_map[st.session_state.current_update_vendor_country]
all_states = State.get_states_of_country(active_country_iso)
state_map = {s.name: s.iso_code for s in all_states} if all_states else {}
state_options = sorted(list(state_map.keys()))

# Ensure selected state is valid for the current country list
if st.session_state.current_update_vendor_state not in state_options:
    st.session_state.current_update_vendor_state = state_options[0] if state_options else None

# B. Get Active Cities matching chosen state
city_options = []
if st.session_state.current_update_vendor_state and state_map:
    active_state_iso = state_map[st.session_state.current_update_vendor_state]
    all_cities = City.get_cities_of_state(active_country_iso, active_state_iso)
    city_options = sorted([c.name for c in all_cities]) if all_cities else []

if st.session_state.current_update_vendor_city not in city_options:
    st.session_state.current_update_vendor_city = city_options[0] if city_options else None


st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Update Vendor </h2>",unsafe_allow_html=True)
st.write("---")

# vendors_df = vendors_df[["id", "vendor_name", "contact_name", "email", "phone_number_calling", "phone_number_whatsapp"]]


    
if vendors_df is not None:
    # Extract the single row as a new DataFrame for editing
    
    st.markdown(f"<h3 style='text-align: center; color: #6B1D1D ;'> Edit Details for vendor: {vendors_df['vendor_name'].values[0]} </h3>",unsafe_allow_html=True)
    st.session_state.edited_df = None
    # Enclose editing and submission inside a Form to control API triggers
    if st.session_state.edited_df is None:
        with st.container(key="storm_box"):
            update_address = st.radio("Do you want to update the address details?", ["Yes", "No"], index = 1, key="update_address", horizontal=True)
            if update_address == "Yes":
                # Reset edited_df on each new selection to avoid stale data issues
                
                edited_df = st.data_editor(
                    vendors_df,
                    disabled=["id","country","state","city", "pincode", "street"], # Prevent the user from tampering with the primary key ID
                    hide_index=True,
                    key="customer_selection"
                )

                # 1. Country Selector Dropdown
                chosen_country = st.selectbox(
                    "Select Country",
                    options=country_names,
                    index=country_names.index(st.session_state.current_update_vendor_country),
                    key="ui_country_node"
                )
                # Check for direct update
                if chosen_country != st.session_state.current_update_vendor_country:
                    st.session_state.current_update_vendor_country = chosen_country
                    st.session_state.current_update_vendor_state = None  # Force child reset
                    st.session_state.current_update_vendor_city = None
                    st.rerun()

                # 2. State Selector Dropdown
                state_index = state_options.index(st.session_state.current_update_vendor_state) if st.session_state.current_update_vendor_state else 0
                chosen_state = st.selectbox(
                    "Select State",
                    options=state_options,
                    index=state_index,
                    disabled=not state_options,
                    key="ui_state_node",
                )
                # Check for direct update
                if chosen_state != st.session_state.current_update_vendor_state:
                    st.session_state.current_update_vendor_state = chosen_state
                    st.session_state.current_update_vendor_city = None  # Force child reset
                    st.rerun()

                # 3. City Selector Dropdown
                city_index = city_options.index(st.session_state.current_update_vendor_city) if st.session_state.current_update_vendor_city else 0
                chosen_city = st.selectbox(
                    "Select City",
                    options=city_options,
                    index=city_index,
                    disabled=not city_options,
                    key="ui_city_node",
                )
                if chosen_city != st.session_state.current_update_vendor_city:
                    st.session_state.current_update_vendor_city = chosen_city

                all_zip_codes = fetch_zip_codes(st.session_state.current_update_vendor_city)
                postal_code = st.selectbox("Postal Code / ZIP",options=all_zip_codes, index = all_zip_codes.index(int(st.session_state.current_update_vendor_pincode)),key="ui_zip_node")
                street = st.text_input("Street Address", key="street_input", value=vendors_df['street'].values[0] if not vendors_df['street'].isna().all() else "")
                
                
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
                            "vendor_name": edited_df['vendor_name'].values[0],
                            "contact_name": edited_df['contact_name'].values[0],
                            "email": edited_df['email'].values[0],
                            "phone_number_calling": edited_df['phone_number_calling'].values[0],
                            "phone_number_whatsapp": edited_df['phone_number_whatsapp'].values[0],
                            "updated_by": st.session_state.get("username", "System"),
                            "vendor_id": str(edited_df['id'].values[0]),
                            "country": edited_df['country'].values[0],
                            "state": edited_df['state'].values[0],
                            "city": edited_df['city'].values[0],
                            "pincode": str(edited_df['pincode'].values[0]),
                            "street": edited_df['street'].values[0]
                        }
                    res = send_post_request('/vendor/update_vendor',payload)
                    if res == 200:
                        st.success("Vendor updated successfully! Navigating to view page...")
                        time.sleep(3)
                        st.session_state.vendors_df = None
                        st.switch_page("views/Vendors/view_vendors.py")
                    else :
                        st.error ("Could not update vendor")
            else:
                # st.session_state.edited_df = True
                edited_df = st.data_editor(
                    vendors_df,
                    disabled=["id","country","state","city", "pincode", "street"], # Prevent the user from tampering with the primary key ID
                    hide_index=True,
                    key="customer_selection"
                )
                submit_button = st.button("Update Vendor")
                if submit_button:
                # payload = edited_df.to_dict(orient='records')[0]
                    payload = {
                            "vendor_name": edited_df['vendor_name'].values[0],
                            "contact_name": edited_df['contact_name'].values[0],
                            "email": edited_df['email'].values[0],
                            "phone_number_calling": edited_df['phone_number_calling'].values[0],
                            "phone_number_whatsapp": edited_df['phone_number_whatsapp'].values[0],
                            "updated_by": st.session_state.get("username", "System"),
                            "vendor_id": str(edited_df['id'].values[0]),
                            "country": None,
                            "state": None, 
                            "city": None,
                            "pincode": None,
                            "street": None
                    }
                    res = send_post_request('/vendor/update_vendor',payload)
                    if res == 200:
                        st.success("Vendor updated successfully! Navigating to view page...")
                        time.sleep(3)
                        st.session_state.vendors_df = None
                        st.switch_page("views/Vendors/view_vendors.py")
                    else:
                        st.error("Could not update vendor")
            if st.button("Go Back to View Page"):
                st.session_state.vendors_df = None
                st.switch_page("views/Vendors/view_vendors.py")
