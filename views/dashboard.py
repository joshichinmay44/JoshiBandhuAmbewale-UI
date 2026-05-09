import streamlit as st

st.title("📊 Enterprise Overview Dashboard")
st.write("Real-time monitoring metrics for mango logistics operations loops.")
st.write("---")

col1, col2, col3 = st.columns(3)
col1.metric("Active Distribution Orders", "412", "+14% This Month")
col2.metric("Dispatched Cold Storage Weight", "3.2 Tons", "Optimal Ops Threshold")
col3.metric("Gross Revenue Realized", "₹8,45,200", "+22%")
