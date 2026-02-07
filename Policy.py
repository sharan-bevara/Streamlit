import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client inside the button click
# so Streamlit UI loads even if OpenAI is missing
st.set_page_config(page_title="Policy Assistant", layout="centered")

st.title("🛡️ Policy Information Assistant")
st.write("Enter your details below 👇")

name = st.text_input("Full Name")
age = st.number_input("Age", 0, 120)
phone = st.text_input("Phone Number")
policy_no = st.text_input("Policy Number")

if st.button("Get Policy Information"):
    if not (name and phone and policy_no):
        st.error("Please fill in all required fields")
    else:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv("sk-...xKEA"))

        # Build the prompt
        prompt = f"""
You are a helpful insurance assistant.

User Details:
Name: {name}
Age: {age}
Phone: {phone}
Policy Number: {policy_no}

Provide a friendly summary of the user's policy including:
- Policy type
- Coverage amount
- Policy status
- Validity
- Any important notes
"""

        with st.spinner("ChatGPT is retrieving policy information..."):
            # Call ChatGPT
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

        # Display result
        st.success("Policy details retrieved!")
        st.subheader("📄 Policy Information")
        st.write(response.output_text)



