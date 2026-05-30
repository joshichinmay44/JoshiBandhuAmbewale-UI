import streamlit as st

col1, col2 = st.columns(2)
with st.expander("Choose appropriate action", expanded=True):
    add_customer_button = st.button("Add New SKu", use_container_width=True)
    if add_customer_button:
        st.switch_page("views/Inventory/add_new_sku.py")
    update_customer_button = st.button("View Existing SKUs", use_container_width=True)
    if update_customer_button:
        st.switch_page("views/Inventory/view_sku.py")
    add_inventory_button = st.button("Add Inventory", use_container_width=True)
    if add_inventory_button:
        st.switch_page("views/Inventory/add_inventory.py")
    view_inventory_button = st.button("View Current Inventory", use_container_width=True)
    if view_inventory_button:
        st.switch_page("views/Inventory/view_current_inventory.py")