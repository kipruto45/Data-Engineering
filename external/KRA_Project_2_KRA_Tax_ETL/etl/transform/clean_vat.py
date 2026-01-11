import os
import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED = os.path.join(BASE, 'data', 'processed')


def clean_vat(df: pd.DataFrame) -> pd.DataFrame:
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    for col in ['transaction_value', 'vat_amount']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    return df


if __name__ == '__main__':
    fn = os.path.join(PROCESSED, 'vat_extracted.csv')
    df = pd.read_csv(fn)
    df = clean_vat(df)
    out = os.path.join(PROCESSED, 'vat_clean.csv')
    df.to_csv(out, index=False)
    print('Cleaned and wrote', out)
