import os
import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED = os.path.join(BASE, 'data', 'processed')


def clean_withholding(df: pd.DataFrame) -> pd.DataFrame:
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
    return df


if __name__ == '__main__':
    fn = os.path.join(PROCESSED, 'withholding_extracted.csv')
    df = pd.read_csv(fn)
    df = clean_withholding(df)
    out = os.path.join(PROCESSED, 'withholding_clean.csv')
    df.to_csv(out, index=False)
    print('Cleaned and wrote', out)
