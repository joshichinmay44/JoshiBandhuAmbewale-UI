import streamlit as st
import requests
from datetime import date
import time

# FastAPI Backend Config
BACKEND_URL = "http://127.0.0.1:8000"

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'>🥭 जोशी बंधू आंबेवाले 🥭</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6B1D1D  ;'>Administrator Registration</h3>", unsafe_allow_html=True)
st.write("---")

min_selectable = date(1930, 1, 1)
max_selectable = date(2056, 12, 31)


_, center_col, _ = st.columns(3)

created_by = st.session_state.get("username", "System")

with center_col:
    with st.form("Registration_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        date_of_birth = st.date_input(
        label="Select Date",
        value=date.today(),       # Default starting point
        min_value=min_selectable, # Expands minimum year limit
        max_value=max_selectable  # Expands maximum year limit
        )
        phone_number = st.text_input("Phone Number")
        address = st.text_area("Address")
        
        submit = st.form_submit_button("Submit")
            
        if submit:
            if not username or not password or not email:
                st.warning("Please fill in both fields.")
            else:
                payload = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
                    "phone_number": phone_number,
                    "address": address,
                    "created_by": created_by
                }
                try:
                    # POST request sent to your FastAPI login router route
                    response = requests.post(f"{BACKEND_URL}/login/add_user", json=payload)
                    
                    # --- CONDITIONAL RESPONSE ROUTING ---
                    if response.status_code == 200:
                        response_data = response.json()
                        
                        # 1. Store token string safely in local memory state
                        # st.session_state.token = response_data.get("access_token")
                        st.session_state.logged_in = False

                        st.success("Registration successful! Redirecting to Login...")

                        time.sleep(3)

                        st.switch_page('views/login.py')
                        
                        st.success("Admin registered successfully! Redirecting...")
                        st.rerun()  # Forces app entrypoint to re-evaluate routing maps immediately
                        
                    elif response.status_code == 401:
                        st.error("❌ Invalid Username or Password. Access Denied.")
                        
                    elif response.status_code == 422:
                        st.error("⚠️ Validation Error: Check input format requirements.")

                    elif response.status_code == 400 :
                        st.error("⚠️ Incorrect username or password.")
                    else:
                        st.error(f"Unexpected status received: {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("💥 Server Unreachable: Ensure your local FastAPI server application is running on port 8000.")
