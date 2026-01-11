import os
import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED = os.path.join(BASE, 'data', 'processed')


def clean_tax_returns(df: pd.DataFrame) -> pd.DataFrame:
    # basic cleaning: parse dates, ensure numeric columns
    if 'period_start' in df.columns:
        df['period_start'] = pd.to_datetime(df['period_start'], errors='coerce')
    if 'period_end' in df.columns:
        df['period_end'] = pd.to_datetime(df['period_end'], errors='coerce')
    for col in ['tax_due', 'tax_paid']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    return df


if __name__ == '__main__':
    fn = os.path.join(PROCESSED, 'tax_returns_extracted.csv')
    df = pd.read_csv(fn)
    df = clean_tax_returns(df)
    out = os.path.join(PROCESSED, 'tax_returns_clean.csv')
    df.to_csv(out, index=False)
    print('Cleaned and wrote', out)
