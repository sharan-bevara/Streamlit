import streamlit as st
import os

st.set_page_config(page_title="Policy Assistant", layout="centered")

st.title("🛡️ Policy Information Assistant")
st.write("Enter your details below 👇")

# UI ALWAYS loads
name = st.text_input("Full Name")
age = st.number_input("Age", 0, 120)
phone = st.text_input("Phone Number")
policy_no = st.text_input("Policy Number")

st.divider()

if st.button("Get Policy Information"):
    if not (name and phone and policy_no):
        st.error("Please fill in all required fields")
    else:
        st.info("UI working fine 👍 (API call will be added next)")
