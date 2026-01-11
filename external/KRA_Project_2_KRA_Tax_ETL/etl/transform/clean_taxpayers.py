import os
import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED = os.path.join(BASE, 'data', 'processed')


def clean_taxpayers(df: pd.DataFrame) -> pd.DataFrame:
    # basic cleaning: trim whitespace, fill missing sectors, standardize dates
    df['name'] = df['name'].str.strip()
    df['sector'] = df['sector'].fillna('Others')
    if 'registration_date' in df.columns:
        df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    return df


if __name__ == '__main__':
    fn = os.path.join(PROCESSED, 'taxpayers_extracted.csv')
    df = pd.read_csv(fn, dtype=str, parse_dates=['registration_date'])
    df = clean_taxpayers(df)
    out = os.path.join(PROCESSED, 'taxpayers_clean.csv')
    df.to_csv(out, index=False)
    print('Cleaned and wrote', out)
