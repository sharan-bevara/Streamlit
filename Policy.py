import streamlit as st
from openai import OpenAI

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Policy Assistant", layout="centered")

# ---------- BACKGROUND IMAGE ----------
def set_bg():
    bg_url = "https://images.unsplash.com/photo-1521791136064-7986c2920216"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{bg_url}");  /* Keeps the background image */
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Main content panel (background and text color) */
        .block-container {{
            background-color: rgba(54, 69, 79, 0.8);  /* Dark blue-gray background with transparency */
            color: #E0E0E0;  /* Light gray text for contrast */
            padding: 2rem;
            border-radius: 15px;
        }}

        /* Headings */
        .block-container h1, 
        .block-container h2, 
        .block-container h3 {{
            color: #E0E0E0;  /* Light headings for readability */
        }}

        /* Buttons */
        .stButton>button {{
            background-color: #00B0FF;  /* Vibrant blue button */
            color: white;
            border-radius: 8px;
        }}

        /* Sidebar background - dark gray / navy */
        [data-testid="stSidebar"] {{
            background-color: #1F1F1F !important;  /* Dark gray / navy */
            color: #E0E0E0 !important;  /* Light text */
        }}

        /* Sidebar text color */
        [data-testid="stSidebar"] * {{
            color: #E0E0E0 !important;  /* Light gray text for readability */
        }}

        /* Top-right menu / header - matching dark theme */
        [data-testid="stHeader"] {{
            background-color: #1F1F1F !important;  /* Dark gray / navy */
        }}

        /* Apply white color to input labels */
        .stTextInput label, .stNumberInput label, .stSelectbox label {{
            color: #FFFFFF !important;  /* White labels for input fields */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg()

# ---------- TITLE ----------
st.title("🛡️ Streamlit")

# ---------- OPENAI ----------
client = OpenAI(api_key=st.secrets["Open_API_Key"])

# ---------- FUNCTIONS ----------

def generate_policy_details(name, age, gender, phone, policy_no, policy_name):

    prompt = f"""
Customer Details:
Name: {name}
Age: {age}
Gender: {gender}
Phone: {phone}
Policy Number: {policy_no}
Policy Name: {policy_name}

Explain the policy clearly with:
- Coverage
- Benefits
- Premium
- Maturity
- Claim process
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an insurance assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def suggest_policies(age, gender):

    prompt = f"""
Suggest 5 best insurance policies for:
Age: {age}
Gender: {gender}

Include:
- policy name
- premium range
- why suitable
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an insurance advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


# ---------- USER INPUT ----------
st.subheader("Enter Customer Details")

name = st.text_input("Full Name")
age = st.number_input("Age", 0, 100)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
phone = st.text_input("Phone Number")
policy_no = st.text_input("Policy Number")
policy_name = st.text_input("Policy Name")

st.divider()

# ---------- BUTTON 1 ----------
if st.button("📄 Generate Policy Details"):
    if not (name and phone and policy_no and policy_name):
        st.error("Please fill all fields")
    else:
        with st.spinner("Generating policy details..."):
            reply = generate_policy_details(
                name, age, gender, phone, policy_no, policy_name
            )

        st.success("Policy Information")
        st.write(reply)

st.divider()

# ---------- BUTTON 2 ----------
if st.button("💡 Suggest More Policies"):
    if age == 0:
        st.error("Please enter age")
    else:
        with st.spinner("Finding best policies..."):
            suggestions = suggest_policies(age, gender)

        st.success("Recommended Policies")
        st.write(suggestions)
