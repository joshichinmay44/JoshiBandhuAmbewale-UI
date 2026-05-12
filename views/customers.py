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


countries = Country.get_countries()
country_names = {c.name: c for c in countries}

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'> Customer Portal  </h2>",unsafe_allow_html=True)
st.write("---")

with st.form("add_customers_form"):
    first_name = st.text_input("first_name", placeholder="e.g. admin")
    last_name = st.text_input("last_name", placeholder="eg. admin")
    email = st.text_input("email", placeholder="e.g. admin@example.com")
    phone_number_calling = st.text_input("phone_number_calling", placeholder="e.g. 123-456-7890")
    phone_number_whatsapp = st.text_input("phone_number_whatsapp", placeholder="e.g. 123-456-7890")
    customer_type = st.selectbox("customer_type", ["Retail", "Wholesale"])
    customer_mode = st.selectbox("customer_mode", ["Online", "Offline"])
    created_by = st.session_state.get("username", "System")  
    st.text("Address Details")
    selected_country_name = st.selectbox("Select Country", options= ["India"] + list([c for c in country_names.keys() if c != "India"]), placeholder="India")
    country = country_names[selected_country_name]
    # --- 2. State Dropdown ---
    states = State.get_states_of_country(country.iso2)
    state_names = {s.name: s for s in states}
    
    selected_state_name = st.selectbox("Select State", options=["Maharashtra"] + list(state_names.keys()), placeholder="Select a country first")
            
    if selected_state_name:
        state = state_names[selected_state_name]
                
    # --- 3. City Dropdown ---
    cities = City.get_cities_of_state(country.iso2,state.iso_code)
    city_names = [c.name for c in cities]
    
    if city_names:
        selected_city = st.selectbox("Select City", options=["Pune"] + city_names)
        
        zip_codes = fetch_zip_codes(selected_city)
        pincode = st.selectbox("Postal/Zip Code", options=zip_codes,index=None, placeholder= 'Please type your pin code to search...')

        address_line_1 =st.text_input("Street Address", placeholder="e.g. 123 Main St, Apt 4B")
        
        address_line_2 = st.text_input("Address Line 2", placeholder="e.g. Landmark, Building Name (Optional)")
        
    submit = st.form_submit_button("Add Customer", use_container_width=True),
    if submit:
        if not first_name or not last_name or not email:
            st.warning("Please fill in all required fields.")
        else:
            payload = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number_calling": phone_number_calling,
                "phone_number_whatsapp": phone_number_whatsapp,
                "customer_type": customer_type,
                "customer_mode": customer_mode,
                "created_by": created_by,
                "country": selected_country_name,
                "state": selected_state_name,
                "city": selected_city,
                "pincode": str(pincode),
                "street": f"{address_line_1}, {address_line_2}"
            }
            try:
                response = requests.post(f"{BACKEND_URL}/customer/add_customer", json=payload)
                if response.status_code == 200:
                    st.success(f"Customer {first_name} {last_name} added successfully!")
                else:
                    st.error(f"Failed to add customer: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error occurred: {e}")

view_customers = st.button("View/Update Customers", use_container_width=True)
if view_customers:
    st.switch_page("views/update_customers.py")
