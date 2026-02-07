import streamlit as st
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Policy ChatGPT Assistant", layout="centered")

st.title("🛡️ Policy Information Assistant")
st.write("Enter your details to get policy information via ChatGPT.")

# User inputs
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
phone = st.text_input("Phone Number")
policy_no = st.text_input("Policy Number")

if st.button("Get Policy Information"):
    if name and phone and policy_no:
        with st.spinner("ChatGPT is analyzing your policy..."):

            prompt = f"""
            You are an insurance assistant.

            User Details:
            Name: {name}
            Age: {age}
            Phone Number: {phone}
            Policy Number: {policy_no}

            Provide a clear and friendly policy summary including:
            - Policy type
            - Coverage amount
            - Policy status
            - Validity
            - Any important notes
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful insurance assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )

            policy_info = response.choices[0].message.content

        st.success("Policy details retrieved!")
        st.subheader("📄 Policy Information")
        st.write(policy_info)

    else:
        st.error("Please fill in all required fields.")
