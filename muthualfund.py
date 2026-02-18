import pandas as pd
import os
import json
from openai import OpenAI

# 🔹 Add your REAL API key here
client = OpenAI(api_key="open ai key")

# Load CSV
file_path = r"C:\Users\sharan\Downloads\SchemeData2301262313SS.csv"
df = pd.read_csv(file_path)

# Get first 10 Scheme NAV Names
scheme_names = df["Scheme NAV Name"].head(50).tolist()

results = []

# Safe float converter (prevents NoneType errors)
def safe_float(value):
    try:
        return float(value)
    except:
        return None

for scheme in scheme_names:
    prompt = f"""
    Provide latest financial data for the mutual fund scheme "{scheme}".

    Return ONLY valid JSON in this exact format:

    {{
        "AUM": number,
        "TER": number,
        "PE": number,
        "PB": number,
        "Sharpe": number,
        "Sortino": number,
        "Age": number,
        "Inception": "YYYY-MM-DD",
        "Top3TotalPercent": number,
        "Top5TotalPercent": number,
        "Top10TotalPercent": number,
        "Top20TotalPercent": number
    }}

    All percentage values must be numeric only (example: 23.45 not "23.45%").
    """

    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=prompt
        )

        data = json.loads(response.output_text)

        results.append({
            "Scheme NAV Name": scheme,
            "AUM (Cr)": safe_float(data.get("AUM")),
            "TER (%)": safe_float(data.get("TER")),
            "PE": safe_float(data.get("PE")),
            "PB": safe_float(data.get("PB")),
            "Sharpe": safe_float(data.get("Sharpe")),
            "Sortino": safe_float(data.get("Sortino")),
            "Age (Years)": safe_float(data.get("Age")),
            "Inception Date": data.get("Inception"),
            "Top 3 Holdings": safe_float(data.get("Top3TotalPercent")),
            "Top 5 Holdings": safe_float(data.get("Top5TotalPercent")),
            "Top 10 Holdings": safe_float(data.get("Top10TotalPercent")),
            "Top 20 Holdings": safe_float(data.get("Top20TotalPercent")),
        })

        print(f" Data fetched for: {scheme}")

    except Exception as e:
        print(f" Error for {scheme}: {e}")

# Convert to DataFrame
result_df = pd.DataFrame(results)

# Save to Excel
excel_file = "MutualFund_Final_Output.xlsx"
result_df.to_excel(excel_file, index=False)

print("\nExcel File Created Successfully!")
print(result_df)

# Auto-open Excel file
os.startfile(excel_file)
