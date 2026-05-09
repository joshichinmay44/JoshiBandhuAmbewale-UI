import streamlit as st

st.markdown("<h2 style='text-align: center; color: #6B1D1D ;'>🥭 Core Vault Inventory Management </h2>",unsafe_allow_html=True)
st.write("---")

# with st.form("add_stock_record"):
#     mango_variety = st.selectbox("Variety Range Selection", ["Alphonso (Ratnagiri)", "Devgad Hapus", "Kesar"])
#     crates_count = st.number_input("Incoming Storage Units (Crates Count)", min_value=1)

col1, col2 = st.columns(2)
with st.expander("Choose appropriate action"):
      if st.button("Manage Customers", use_container_width=True):
          st.switch_page("views/customers.py")

# with col2:
#     if st.button("🧾 View Customer Orders", use_container_width=True):
#         st.switch_page("views/orders.py") # Assumes this file exists