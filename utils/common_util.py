import streamlit as st
import requests
BACKEND_URL = "http://127.0.0.1:8000"

def circular_spinner(text="Loading data..."):
    return st.html(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 30px 0;">
            <div style="
                border: 5px solid #5C3D2E; 
                border-top: 5px solid #FF4B4B; 
                border-radius: 50%;
                width: 45px;
                height: 45px;
                animation: spin 1s linear infinite;
            "></div>
            <p style="font-family: sans-serif; color: #6B1D1D; margin-top: 15px; font-size: 30px;">{text}</p>
        </div>
        <style>
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
        """
    )

def fetch_zip_codes(city :str):
    try:
        response = requests.get(f"{BACKEND_URL}/address/get_pin_codes/{city}")
        if response.status_code == 200:
            return response.json().get("pin_codes", [])
        else:
            raise Exception(f"Failed to fetch zip codes: {response.text}")

    except Exception as e:
        raise Exception(f"Error occurred while fetching zip codes: {e}")

def send_post_request(sub_domain, payload):
    try:
        response = requests.post(f"{BACKEND_URL}/{sub_domain}", json=payload)
        return response.status_code
    except Exception as e:
        st.error(f"Error occurred while updating customer: {e}")