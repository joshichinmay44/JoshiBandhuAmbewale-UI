import streamlit as st
from utils.common_util import send_post_request

BACKEND_URL = "http://127.0.0.1:8000"


@st.fragment
def add_sku_form():
    with st.container(key="storm_box"):
        st.write("### New Vendor Details")
        sku_name = st.text_input("SKU Name", placeholder="e.g. 2.5 dozen")
        description = st.text_input("Description", placeholder="eg. 30 mangoes packed in a box")
        if st.button("Save SKU Details", type="primary"):
            payload = {
                            "sku_name": sku_name,
                            "description": description,
                            "created_by": st.session_state.username
                        }
            res = send_post_request('sku/add_sku',payload)
            if res == 200:
                st.success("SKU added successfully")
            else:
                st.error(f"Failed to add SKU. Please try again. Error: {res}")
        else:
            if not sku_name or not description:
                st.error("Please complete all location fields before submitting.")
        if st.button("View/Update SKUs", type="primary"):
            st.switch_page("views/Inventory/view_sku.py")


add_sku_form()