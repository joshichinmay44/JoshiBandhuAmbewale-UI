import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

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
        created_by = st.session_state.get("username", "System")  # Default to "Unknown User" if not set
        submit = st.form_submit_button("Add Customer", use_container_width=True)
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
                    "created_by": created_by
                }
                try:
                    response = requests.post(f"{BACKEND_URL}/customer/add_customer", json=payload)
                    if response.status_code == 200:
                        st.success(f"Customer {first_name} {last_name} added successfully!")
                    else:
                        st.error(f"Failed to add customer: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error occurred: {e}")
response = requests.get(f"{BACKEND_URL}/customer/get_customers")
if response.status_code == 200:
    customers = response.json()['customers']
    customers_df= pd.DataFrame(customers)
    customers_df.drop(columns=[0], inplace=True)  # Drop the 'id' column for cleaner display
    st.subheader("Interactive Table")
    st.dataframe(customers_df,use_container_width=True,column_config={
        "1": "First Name",
        "2": "Last Name",
        "3": "Email",
        "4": "Calling Number",
        "5": "WhatsApp Number",
        "6": "Customer Type",
        "7": "Customer Mode",
        "8": "Created At",
        "9": "Updated At",
        "10": "Created By",
        "11": "Updated By" 
    })

    if st.button("Update Customers", use_container_width=True):
        st.switch_page("views/update_customers.py")
