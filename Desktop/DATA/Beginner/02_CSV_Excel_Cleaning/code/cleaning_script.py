"""CSV and Excel cleaning starter script

Usage:
    python cleaning_script.py

Note: this script demonstrates basic cleaning. Replace `data/raw/sample.xlsx` with
an actual Excel file and update as needed.
"""

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_XLSX = ROOT / "data" / "raw" / "sample.xlsx"
RAW_CSV = ROOT / "data" / "raw" / "sample.csv"
CLEANED = ROOT / "data" / "cleaned" / "cleaned_sample.csv"


def load(path):
    if path.suffix == ".xlsx":
        return pd.read_excel(path)
    return pd.read_csv(path)


def clean(df):
    # example cleaning: drop entirely empty rows and strip column names
    df = df.dropna(how="all")
    df.columns = [c.strip() for c in df.columns]
    return df


if __name__ == "__main__":
    # prefer CSV if present, otherwise Excel
    path = RAW_CSV if RAW_CSV.exists() else RAW_XLSX
    if not path.exists():
        print("No sample data found. Please add `sample.csv` or `sample.xlsx` to data/raw/")
    else:
        df = load(path)
        df = clean(df)
        df.to_csv(CLEANED, index=False)
        print(f"Cleaned data written to {CLEANED}")
