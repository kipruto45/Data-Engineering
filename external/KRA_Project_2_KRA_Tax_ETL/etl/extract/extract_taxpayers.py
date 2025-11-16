import os
import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RAW = os.path.join(BASE, 'data', 'raw')
PROCESSED = os.path.join(BASE, 'data', 'processed')
os.makedirs(PROCESSED, exist_ok=True)


def extract_taxpayers():
    fn = os.path.join(RAW, 'taxpayers_raw.csv')
    df = pd.read_csv(fn, dtype=str)
    out = os.path.join(PROCESSED, 'taxpayers_extracted.csv')
    df.to_csv(out, index=False)
    return df


if __name__ == '__main__':
    df = extract_taxpayers()
    print('Extracted', len(df), 'taxpayers')
