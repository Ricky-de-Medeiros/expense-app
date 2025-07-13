import pandas as pd

def load_transactions(csv_file: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    # Basic normalization — customize per bank format
    df.columns = df.columns.str.strip().str.lower()
    return df

def tag_business_expenses(df: pd.DataFrame, rules: dict = None) -> pd.DataFrame:
    df["is_business"] = False
    df["category"] = "Uncategorized"

    if rules:
        for keyword, category in rules.items():
            matches = df["description"].str.contains(keyword, case=False, na=False)
            df.loc[matches, "is_business"] = True
            df.loc[matches, "category"] = category

    return df
