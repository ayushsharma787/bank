import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "UniversalBank.csv"

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    # Drop irrelevant columns
    df = df.drop(columns=["ID", "ZIP Code"], errors="ignore")
    # Fix negative experience
    df["Experience"] = df["Experience"].clip(lower=0)
    return df

def get_feature_target(df: pd.DataFrame):
    target = "Personal Loan"
    features = [c for c in df.columns if c != target]
    X = df[features]
    y = df[target]
    return X, y, features

def get_summary_stats(df: pd.DataFrame) -> dict:
    loan_col = "Personal Loan"
    accepted = int(df[loan_col].sum())
    total = len(df)
    avg_income = float(df["Income"].mean())
    avg_cc = float(df["CCAvg"].mean())
    avg_age = float(df["Age"].mean())
    avg_mortgage = float(df[df["Mortgage"] > 0]["Mortgage"].mean())
    online_pct = float(df["Online"].mean() * 100)
    cc_holders_pct = float(df["CreditCard"].mean() * 100)
    securities_pct = float(df["Securities Account"].mean() * 100)
    cd_pct = float(df["CD Account"].mean() * 100)

    return {
        "total_customers": total,
        "loan_accepted": accepted,
        "loan_rejected": total - accepted,
        "acceptance_rate": round(accepted / total * 100, 2),
        "avg_income": round(avg_income, 1),
        "avg_cc": round(avg_cc, 2),
        "avg_age": round(avg_age, 1),
        "avg_mortgage": round(avg_mortgage, 1),
        "online_pct": round(online_pct, 1),
        "cc_holders_pct": round(cc_holders_pct, 1),
        "securities_pct": round(securities_pct, 1),
        "cd_pct": round(cd_pct, 1),
    }
