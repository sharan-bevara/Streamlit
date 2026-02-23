import pandas as pd
import json
import asyncio
import os
import sys
import streamlit as st
from openai import AsyncOpenAI

# ================== CONFIG ==================
API_KEY = "sk-REPLACE_WITH_YOUR_KEY"   # 🔴 use Streamlit secrets in production

CSV_FILE = "/Users/s-hydfrontdesk/Downloads/SchemeData2301262313SS.csv"
OUTPUT_FILE = "MutualFund_Final_Output.xlsx"

MAX_FUNDS = None              # None = all funds
MAX_CONCURRENT_REQUESTS = 5
MODEL = "gpt-4.1"
# ============================================


def safe_float(value, default=0):
    try:
        return float(value)
    except:
        return default


def validate_weightage_sum(weightage):
    total = sum(weightage.values())
    if total != 100:
        raise ValueError(f"❌ Weightage sum must be 100, but got {total}")
    print("✅ Weightage validation passed (Total = 100)")


async def fetch_scheme_data(scheme, client, semaphore):
    prompt = f"""
    Provide financial data for the mutual fund scheme "{scheme}".

    Return ONLY valid JSON:
    {{
        "AUM": number,
        "TER": number,
        "PE": number,
        "PB": number,
        "Top3TotalPercent": number,
        "Top5TotalPercent": number,
        "Top10TotalPercent": number,
        "Top20TotalPercent": number,
        "Sharpe": number,
        "Sortino": number,
        "StdDev": number,
        "InceptionReturn": number,
        "Age": number
    }}
    """

    async with semaphore:
        try:
            response = await client.responses.create(
                model=MODEL,
                input=prompt
            )

            data = json.loads(response.output_text)

            return {
                "Fund Name": scheme,
                "AUM": safe_float(data.get("AUM")),
                "TER": safe_float(data.get("TER")),
                "PE": safe_float(data.get("PE")),
                "PB": safe_float(data.get("PB")),
                "Top 3 Holdings": safe_float(data.get("Top3TotalPercent")),
                "Top 5 Holdings": safe_float(data.get("Top5TotalPercent")),
                "Top 10 Holdings": safe_float(data.get("Top10TotalPercent")),
                "Top 20 Holdings": safe_float(data.get("Top20TotalPercent")),
                "Sharpe": safe_float(data.get("Sharpe")),
                "Sortino": safe_float(data.get("Sortino")),
                "Std Dev": safe_float(data.get("StdDev")),
                "Inception %": safe_float(data.get("InceptionReturn")),
                "Age (Years)": safe_float(data.get("Age")),
            }

        except Exception as e:
            print(f"\n⚠️ Error fetching {scheme}: {e}")
            return None


async def main():
    client = AsyncOpenAI(api_key=API_KEY)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    # ---------------- READ CSV ----------------
    df = pd.read_csv(CSV_FILE)

    required_cols = ["Scheme NAV Name", "Scheme Category"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"❌ Missing required columns: {missing}")

    # ---------------- FILTER: EQUITY SCHEME ----------------
    df["Category_Main"] = (
        df["Scheme Category"]
        .astype(str)
        .str.split("-", n=1)
        .str[0]
        .str.strip()
    )

    equity_df = df[df["Category_Main"] == "Equity Scheme"]

    schemes = (
        equity_df["Scheme NAV Name"]
        .dropna()
        .unique()
        .tolist()
    )

    schemes = schemes[:MAX_FUNDS] if MAX_FUNDS else schemes
    total = len(schemes)

    st.write(f"✅ Selected **{total}** Equity Scheme funds")

    # ---------------- ASYNC FETCH ----------------
    tasks = [fetch_scheme_data(s, client, semaphore) for s in schemes]

    results = []
    progress = st.progress(0)
    completed = 0

    for coro in asyncio.as_completed(tasks):
        result = await coro
        completed += 1

        if result:
            results.append(result)

        progress.progress(completed / total)

    st.success("✅ All funds processed")

    # ---------------- DATAFRAME ----------------
    columns = [
        "Fund Name", "AUM", "TER", "PE", "PB",
        "Top 3 Holdings", "Top 5 Holdings",
        "Top 10 Holdings", "Top 20 Holdings",
        "Sharpe", "Sortino", "Std Dev",
        "Inception %", "Age (Years)"
    ]

    data_df = pd.DataFrame(results, columns=columns)

    # ---------------- WEIGHTAGE ----------------
    weightage = {
        "AUM": 9, "TER": 8, "PE": 7, "PB": 7,
        "Top 3 Holdings": 6, "Top 5 Holdings": 6,
        "Top 10 Holdings": 6, "Top 20 Holdings": 6,
        "Sharpe": 15, "Sortino": 13,
        "Std Dev": 9, "Inception %": 3,
        "Age (Years)": 5
    }

    higher_lower = {
        "AUM": "Higher", "TER": "Lower", "PE": "Lower", "PB": "Lower",
        "Top 3 Holdings": "Higher", "Top 5 Holdings": "Higher",
        "Top 10 Holdings": "Higher", "Top 20 Holdings": "Higher",
        "Sharpe": "Higher", "Sortino": "Higher",
        "Std Dev": "Lower", "Inception %": "Higher",
        "Age (Years)": "Higher"
    }

    validate_weightage_sum(weightage)

    # ---------------- SCORE ----------------
    scores = []

    for _, row in data_df.iterrows():
        score = 0
        for col, wt in weightage.items():
            val = safe_float(row[col])
            score += wt * val if higher_lower[col] == "Higher" else -wt * val
        scores.append(score)

    data_df["Score"] = scores

    # ---------------- SORT + RANK ----------------
    data_df = data_df.sort_values(
        by=["Score", "Fund Name"],
        ascending=[False, True]
    ).reset_index(drop=True)

    data_df["Rank"] = (
        data_df["Score"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    # ---------------- FINAL OUTPUT ----------------
    weightage_row = {"Fund Name": "Weightage", **weightage, "Score": "", "Rank": ""}
    hl_row = {"Fund Name": "Higher/Lower", **higher_lower, "Score": "", "Rank": ""}

    final_df = pd.concat(
        [pd.DataFrame([weightage_row]), pd.DataFrame([hl_row]), data_df],
        ignore_index=True
    )

    final_df.to_excel(OUTPUT_FILE, index=False)

    st.dataframe(final_df, use_container_width=True)

    return OUTPUT_FILE


# ================= STREAMLIT UI =================
if __name__ == "__main__":

    st.set_page_config(page_title="Mutual Fund Scoring Engine", layout="wide")

    st.title("📊 Mutual Fund Scoring Engine")
    st.write("Fetch → Score → Rank → Export mutual funds")

    if st.button("🚀 Run Analysis"):
        with st.spinner("Processing funds..."):
            output_file = asyncio.run(main())

        st.success("🎉 Analysis completed")

        with open(output_file, "rb") as f:
            st.download_button(
                "⬇️ Download Excel Output",
                f,
                file_name=OUTPUT_FILE,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
