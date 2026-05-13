import streamlit as st

col1, col2 = st.columns(2)
with st.expander("Choose appropriate action", expanded=True):
    add_customer_button = st.button("Add New Customers", use_container_width=True)
    if add_customer_button:
        st.switch_page("views/new_customers.py")
    update_customer_button = st.button("Update Existing Customers", use_container_width=True)
    if update_customer_button:
        st.switch_page("views/update_customers.py")
    
    

