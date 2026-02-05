import streamlit as st

st.title("Insurance Policy Application")

# Use a form to batch inputs
with st.form("policy_form"):
    st.header("Customer Details")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=18, max_value=100)
    email = st.text_input("Email")
    
    st.header("Policy Details")
    policy_type = st.selectbox("Policy Type", ["Health", "Life", "Vehicle"])
    coverage = st.slider("Coverage Amount ($)", 10000, 1000000, 50000)
    smoker = st.checkbox("Smoker (for health/life)")
    
    submitted = st.form_submit_button("Apply for Policy")

if submitted:
    # Simple premium calculation logic (base + age factor + smoker premium)
    base_premium = coverage * 0.005  # 0.5% of coverage
    age_factor = (age - 18) * 10
    smoker_premium = 500 if smoker and policy_type in ["Health", "Life"] else 0
    total_premium = base_premium + age_factor + smoker_premium
    
    st.success("Policy Applied Successfully!")
    st.write(f"**Name:** {name}")
    st.write(f"**Policy:** {policy_type}")
    st.write(f"**Coverage:** ${coverage:,.0f}")
    st.write(f"**Annual Premium:** ${total_premium:,.2f}")
    st.balloons()
else:
    if name:  # Preview if partially filled
        st.info("Fill all fields and submit to apply.")
