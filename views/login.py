import streamlit as st
import requests

# FastAPI Backend Config
BACKEND_URL = "http://127.0.0.1:8000"

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'>🥭 जोशी बंधू आंबेवाले 🥭</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6B1D1D  ;'>Administrator Portal</h3>", unsafe_allow_html=True)
st.write("---")

_, center_col, _ = st.columns(3)

with center_col:
    with st.form("login_credentials_form"):
        username = st.text_input("Username", placeholder="e.g. admin")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.warning("Please fill in both fields.")
            else:
                # --- FASTAPI REQUEST EXECUTION ---
                # FastAPI OAuth2PasswordBearer expects application/x-www-form-urlencoded data
                payload = {"username": username, "password": password}
                try:
                    # POST request sent to your FastAPI login router route
                    response = requests.post(f"{BACKEND_URL}/login/token", json=payload)
                    
                    # --- CONDITIONAL RESPONSE ROUTING ---
                    if response.status_code == 200:
                        response_data = response.json()
                        
                        # 1. Store token string safely in local memory state
                        # st.session_state.token = response_data.get("access_token")
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        
                        st.success("Authorization Verified! Redirecting...")
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
    register_button = st.button("Register New Admin", type="secondary", use_container_width=True)
    if register_button:
        st.switch_page("views/register_admin.py")
        
