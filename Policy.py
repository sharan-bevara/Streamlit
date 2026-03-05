import streamlit as st
import pandas as pd
import uuid
import os
from datetime import datetime

# --- CONFIGURATION & STORAGE ---
DISCLOSURES_FILE = 'disclosures.parquet'
INVENTORS_FILE = 'inventors.parquet'

# Define empty schemas for initial file creation
empty_disclosures = pd.DataFrame(columns=[
    'disclosure_id', 'title', 'summary', 'conception_date', 
    'is_publicly_disclosed', 'disclosure_date', 'disclosure_circumstances',
    'is_planned_disclosure', 'planned_disclosure_date', 'strategic_impact_score',
    'description_problem', 'description_longstanding', 'description_differences',
    'description_advantages', 'description_how_it_works', 'description_components',
    'description_implementation', 'description_alternatives', 'description_usage',
    'has_prototype', 'documentation_links', 'third_party_involved', 
    'third_party_involved_exp', 'third_party_interested', 'third_party_interest_exp',
    'submitted_at'
])

empty_inventors = pd.DataFrame(columns=[
    'inventor_id', 'disclosure_id', 'full_name', 'email_address', 
    'country', 'is_former_employee'
])

# --- HELPER FUNCTIONS ---
def load_data(file_name, empty_df):
    if os.path.exists(file_name):
        return pd.read_parquet(file_name)
    return empty_df

def save_data(file_name, new_data_list, empty_df):
    existing_df = load_data(file_name, empty_df)
    new_df = pd.DataFrame(new_data_list)
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    updated_df.to_parquet(file_name, engine='pyarrow')

# --- SESSION STATE INITIALIZATION ---
# We use session state to track dynamic UI elements like adding multiple inventors
if 'inventor_count' not in st.session_state:
    st.session_state.inventor_count = 1

def add_inventor():
    st.session_state.inventor_count += 1

# --- APP UI ---
st.set_page_config(page_title="Patent Disclosure Portal", layout="wide")
st.title("Patent Management & Disclosure Portal")
st.write("Please fill out the form below to submit a new invention disclosure.")

# We do not use st.form here because we need dynamic buttons (Add Inventor) to update the UI instantly
st.header("1. Inventor Information")
inventors_data = []

for i in range(st.session_state.inventor_count):
    st.subheader(f"Inventor {i+1}")
    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
    with col1:
        name = st.text_input("Full Name", key=f"name_{i}")
    with col2:
        email = st.text_input("Email Address", key=f"email_{i}")
    with col3:
        country = st.text_input("Country of Location", key=f"country_{i}")
    with col4:
        st.write("") # Spacing
        st.write("")
        is_former = st.checkbox("Former Employee", key=f"former_{i}")
    
    inventors_data.append({
        "full_name": name,
        "email_address": email,
        "country": country,
        "is_former_employee": is_former
    })

st.button("➕ Add Another Inventor", on_click=add_inventor)
st.divider()

# --- MAIN FORM FIELDS ---
st.header("2. Innovation Timeline / Key Dates")
conception_date = st.text_input("When was the invention conceived? (MM/YY)")

col_pub1, col_pub2 = st.columns(2)
with col_pub1:
    is_public = st.radio("Has the invention been publicly disclosed?", ["No", "Yes"])
    if is_public == "Yes":
        disclosure_date = st.text_input("Disclosure Date (MM/YY)")
        disclosure_circumstances = st.text_area("Circumstances of disclosure")
    else:
        disclosure_date, disclosure_circumstances = None, None

with col_pub2:
    if is_public == "No":
        is_planned = st.radio("Is there a planned disclosure?", ["No", "Yes"])
        if is_planned == "Yes":
            planned_date = st.text_input("Planned Disclosure Date (MM/YY)")
        else:
            planned_date = None
    else:
        is_planned, planned_date = None, None

st.divider()

st.header("3. Strategic Business Impact")
st.write("On a scale of 1 to 3 (1 being the highest), please rate the impact of this invention:")
impact_score_str = st.radio(
    "Impact Level",
    options=[
        "1 - Intended to position the company as a new market leader.",
        "2 - Customers likely to buy our offering over others, but likely not a new market leader.",
        "3 - Generally comparable to competitive offerings; impact unclear."
    ]
)
impact_score = int(impact_score_str[0]) # Extract the number 1, 2, or 3

st.divider()

st.header("4. Invention Details")
title = st.text_input("Title of the Invention")
summary = st.text_area("Brief Summary (1-2 sentences)")
desc_problem = st.text_area("What problem does the invention solve?")
desc_longstanding = st.radio("Does the invention resolve a long-standing problem in the industry?", ["No", "Yes"])
desc_diff = st.text_area("How is your invention different from existing products or solutions?")
desc_adv = st.text_area("What are the advantages or improvements over prior solutions?")
desc_how = st.text_area("How does it work?")
desc_comp = st.text_area("What are its components or steps?")
desc_impl = st.text_area("How are these components and/or steps implemented?")
desc_alt = st.text_area("Are there any alternative ways to make or use your invention?")
desc_usage = st.text_area("How is it used?")
has_prototype = st.radio("Has a prototype been built?", ["No", "Yes"])
doc_links = st.text_area("Other (attach links to documentation, comma separated)")

st.divider()

st.header("5. 3rd Party Involvement")
col_3rd1, col_3rd2 = st.columns(2)
with col_3rd1:
    third_party_inv = st.radio("Was there a 3rd party involved in conceiving or developing this invention?", ["No", "Yes"])
    if third_party_inv == "Yes":
        third_party_inv_exp = st.text_area("Please explain involvement:")
    else:
        third_party_inv_exp = None

with col_3rd2:
    third_party_int = st.radio("Are you aware of any 3rd parties who may be or is already interested?", ["No", "Yes"])
    if third_party_int == "Yes":
        third_party_int_exp = st.text_area("Please explain interest:")
    else:
        third_party_int_exp = None

st.divider()

# --- SUBMISSION LOGIC ---
if st.button("Submit Disclosure", type="primary"):
    # Generate a unique ID for this disclosure
    disclosure_id = str(uuid.uuid4())
    
    # 1. Prepare Main Disclosure Data
    disclosure_record = {
        'disclosure_id': disclosure_id,
        'title': title,
        'summary': summary,
        'conception_date': conception_date,
        'is_publicly_disclosed': True if is_public == "Yes" else False,
        'disclosure_date': disclosure_date,
        'disclosure_circumstances': disclosure_circumstances,
        'is_planned_disclosure': True if is_planned == "Yes" else False,
        'planned_disclosure_date': planned_date,
        'strategic_impact_score': impact_score,
        'description_problem': desc_problem,
        'description_longstanding': True if desc_longstanding == "Yes" else False,
        'description_differences': desc_diff,
        'description_advantages': desc_adv,
        'description_how_it_works': desc_how,
        'description_components': desc_comp,
        'description_implementation': desc_impl,
        'description_alternatives': desc_alt,
        'description_usage': desc_usage,
        'has_prototype': True if has_prototype == "Yes" else False,
        'documentation_links': doc_links,
        'third_party_involved': True if third_party_inv == "Yes" else False,
        'third_party_involved_exp': third_party_inv_exp,
        'third_party_interested': True if third_party_int == "Yes" else False,
        'third_party_interest_exp': third_party_int_exp,
        'submitted_at': datetime.now().isoformat()
    }
    
    # 2. Prepare Inventors Data (linking via disclosure_id)
    final_inventors = []
    for inv in inventors_data:
        # Only save if a name was actually entered
        if inv['full_name'].strip() != "":
            inv['inventor_id'] = str(uuid.uuid4())
            inv['disclosure_id'] = disclosure_id
            final_inventors.append(inv)
            
    # 3. Save to Parquet Files
    try:
        save_data(DISCLOSURES_FILE, [disclosure_record], empty_disclosures)
        if final_inventors:
            save_data(INVENTORS_FILE, final_inventors, empty_inventors)
            
        st.success(f"Successfully submitted! Disclosure ID: {disclosure_id}")
        st.balloons()
    except Exception as e:
        st.error(f"An error occurred while saving: {e}")
