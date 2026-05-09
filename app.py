import streamlit as st
import base64

# --- PAGE INITIALIZATION & CONFIG ---
st.set_page_config(page_title="जोशी बंधू आंबेवाले", page_icon="🥭", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- UTILITY: INJECT LOCAL BACKGROUND IMAGE WITH CSS ---
def set_custom_background(image_path: str):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Injects CSS targeting the main app canvas overlay container
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.3)), 
                                  url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* Makes UI input forms stand out cleanly against custom background */
            .stForm, div[data-testid="stExpander"] {{
                background-color: #5C3D2E !important;
                border-radius: 12px !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
            }}
            /* Target standard secondary buttons on hover */
            .mango-btn div[data-testid="stBaseButton-secondary"]:hover {{
                background-color: #f0f2f6 !important;
                color: #31333F !important;
                border-color: #ff4b4b !important;
            }}
            
            /* Target primary buttons on hover */
            .mango-btn div[data-testid="stBaseButton-primary"]:hover {{
                background-color: #ff4b4b !important;
                color: white !important;
                border-color: #ff4b4b !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        # Fallback to smooth mango-themed gradient overlay if your asset file is missing
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #fef9e7 0%, #fde4c3 100%);
            }
            
            </style>
            """,
            unsafe_allow_html=True
        )

# Execute background injection styling rules
set_custom_background("assets/logo.png")

# --- MULTI-PAGE ROUTING LAYER ---
# Declare sub-page views targeting isolated python files inside the layout directory 
login_page = st.Page("views/login.py", title="Log In", icon="🔒")
dash_page = st.Page("views/dashboard.py", title="Dashboard", icon="📊")
inv_page = st.Page("views/inventory.py", title="Manage Inventory", icon="📦")
customers_page = st.Page("views/customers.py", title="Customer Portal", icon="👥")

# (Keep your existing background configurations at the top of your app.py file)

# Enforce route visualization mapping based on current login authentication checks
if not st.session_state.logged_in:
    pg = st.navigation([login_page], position="hidden") 
else:
    # Adding a global logout mechanism directly inside the sidebar header
    if st.sidebar.button("Log Out", type="primary", use_container_width=True):
        st.session_state.token = None
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Session cleared.")
        st.rerun() # Instantly locks down the pages and routes user back to login view

    pg = st.navigation({
        "Admin Controls": [inv_page , dash_page, customers_page]
    }, position="sidebar")

pg.run()

