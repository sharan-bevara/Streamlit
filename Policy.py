import streamlit as st
import os
from openai import OpenAI

# ---------- CHATGPT FUNCTION ----------
client = OpenAI(api_key=os.getenv("sk-...xKEA"))

def get_policy_response(name, age, phone, policy_no):
    prompt = f"""
    Name: {name}
    Age: {age}
    Phone: {phone}
    Policy Number: {policy_no}

    Provide policy info clearly.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful insurance assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# ---------- UI ----------
st.set_page_config(page_title="Policy Assistant", layout="centered")

st.title("🛡️ Policy Information Assistant")
st.write("Enter your details below 👇")

name = st.text_input("Full Name")
age = st.number_input("Age", 0, 120)
phone = st.text_input("Phone Number")
policy_no = st.text_input("Policy Number")

st.divider()

if st.button("Get Policy Information"):
    if not (name and phone and policy_no):
        st.error("Please fill in all required fields")
    else:
        reply = get_policy_response(name, age, phone, policy_no)
        st.write(reply)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

st.title("Policy Assistant")

name = st.text_input("Name")
policy = st.text_input("Policy number")

if st.button("Check"):
    if name and policy:
        reply = ask_gpt(f"Give policy info for {name} with policy {policy}")
        st.write(reply)
    else:
        st.error("Fill all fields")
        
        

