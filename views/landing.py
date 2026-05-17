import streamlit as st

st.markdown(f"<h2 style='text-align: center; color: #6B1D1D ;'> Welcome {st.session_state.username}</h2>",unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)
with st.expander("Choose appropriate action", expanded = True):
      if st.button("Manage Customers", use_container_width=True):
          st.switch_page("views/customers.py")
      if st.button("Manage Vendors", use_container_width=True):
           st.switch_page("views/new_vendors.py")

# with col2:
#     if st.button("🧾 View Customer Orders", use_container_width=True):
#         st.switch_page("views/orders.py") # Assumes this file exists