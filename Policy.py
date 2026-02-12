import streamlit as st
import openai
import os

# Set your OpenAI API key using Streamlit's secrets management (no hardcoding the API key)
openai.api_key = st.secrets["openai"]["api_key"]

# Function to query GPT for policy details
def get_policy_details(username, age, gender, phone_number, policy_number, policy_name):
    prompt = f"""
    Given the following details:
    - Username: {username}
    - Age: {age}
    - Gender: {gender}
    - Phone Number: {phone_number}
    - Policy Number: {policy_number}
    - Policy Name: {policy_name}
    
    Please provide the exact policy details for the given information. Include coverage, benefits, and any important information related to the policy number {policy_number} and policy name {policy_name}.
    """
    
    try:
        # Request to OpenAI's GPT model
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides accurate policy details."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit UI
st.title('Policy Details Finder')

# User Inputs
username = st.text_input("Enter your Username:")
age = st.number_input("Enter your Age:", min_value=18, max_value=120)
gender = st.selectbox("Select your Gender:", ["Male", "Female", "Other"])
phone_number = st.text_input("Enter your Indian Phone Number:", max_chars=10)
policy_number = st.text_input("Enter your Policy Number:")
policy_name = st.text_input("Enter your Policy Name:")

# Submit Button
if st.button("Get Policy Details"):
    # Validate the inputs
    if len(phone_number) == 10 and phone_number.isdigit():
        if username and policy_number and policy_name:
            with st.spinner("Getting policy details..."):
                # Get policy details from GPT
                policy_details = get_policy_details(username, age, gender, phone_number, policy_number, policy_name)
                if policy_details:
                    # Show the results
                    st.subheader("Policy Details")
                    st.write(policy_details)
                else:
                    st.error("No details found for the given policy.")
        else:
            st.error("Please fill in all the required fields.")
    else:
        st.error("Please enter a valid 10-digit phone number.")
