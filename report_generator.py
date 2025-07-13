import pandas as pd

def calculate_business_percentages(df: pd.DataFrame) -> pd.DataFrame:
    total_spend = df[df["amount"] < 0]["amount"].sum()
    business_spend = df[(df["is_business"]) & (df["amount"] < 0)]["amount"].sum()
    business_pct = (business_spend / total_spend) * 100 if total_spend else 0

    df["business_usage_pct"] = round(business_pct, 2)
    return df

def export_report(df: pd.DataFrame, output_file: str):
    df_sorted = df.sort_values(by="date")

    summary = pd.DataFrame([{
        "date": "TOTAL",
        "description": f"{df['is_business'].sum()} business transactions",
        "amount": df["amount"].sum(),
        "is_business": "",
        "category": "",
        "business_usage_pct": df["business_usage_pct"].iloc[0] if not df.empty else ""
    }])

    final = pd.concat([df_sorted, summary], ignore_index=True)
    final.to_csv(output_file, index=False)
    print(f"✅ Final report saved to {output_file}")
