import streamlit as st

col1, col2 = st.columns(2)
with st.expander("Choose appropriate action", expanded=True):
    add_bookings_button = st.button("Add New Booking", use_container_width=True)
    if add_bookings_button:
        st.switch_page("views/Sales/new_booking.py")
    view_bookings_button = st.button("View Current Bookings", use_container_width=True)
    if view_bookings_button:
        st.switch_page("Views/Sales/view_bookings.py")
    # update_customer_button = st.button("View Existing Vendors", use_container_width=True)
    # if update_customer_button:
    #     st.switch_page("views/Vendors/view_vendors.py")
    
    

