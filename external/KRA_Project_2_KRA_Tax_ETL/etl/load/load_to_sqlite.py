import os
import pandas as pd
from sqlalchemy import create_engine, text

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(BASE, 'kra_tax.db')
PROCESSED = os.path.join(BASE, 'data', 'processed')


def create_conn():
    engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
    return engine


def ensure_tables(engine):
    # create minimal dimension and fact tables if not exist
    with engine.connect() as conn:
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS dim_taxpayer (
                taxpayer_id INTEGER PRIMARY KEY,
                name TEXT,
                pin TEXT,
                registration_date DATE,
                sector TEXT,
                region TEXT
            );
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS dim_date (
                date_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                year INTEGER,
                month INTEGER,
                day INTEGER
            );
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS fact_tax_returns (
                return_id INTEGER PRIMARY KEY,
                taxpayer_id INTEGER,
                period_start DATE,
                period_end DATE,
                tax_due REAL,
                tax_paid REAL,
                filing_date DATE
            );
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS fact_withholding (
                withholding_id INTEGER PRIMARY KEY,
                taxpayer_id INTEGER,
                amount REAL,
                date DATE,
                payer TEXT
            );
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS fact_vat (
                vat_id INTEGER PRIMARY KEY,
                taxpayer_id INTEGER,
                transaction_value REAL,
                vat_amount REAL,
                date DATE
            );
        '''))


def load_csv_to_table(engine, csv_path, table_name, dtype=None, parse_dates=None, if_exists='append'):
    if not os.path.exists(csv_path):
        print('Missing', csv_path)
        return 0
    df = pd.read_csv(csv_path, dtype=dtype, parse_dates=parse_dates)
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    print(f'Loaded {len(df)} rows into {table_name}')
    return len(df)


def upsert_csv_to_table(engine, csv_path, table_name, pk, dtype=None, parse_dates=None):
    """Idempotent upsert: read existing table, merge, drop duplicates by pk, replace table."""
    if not os.path.exists(csv_path):
        print('Missing', csv_path)
        return 0
    new_df = pd.read_csv(csv_path, dtype=dtype, parse_dates=parse_dates)
    # if table exists, merge
    try:
        existing = pd.read_sql_table(table_name, engine)
        combined = pd.concat([existing, new_df], ignore_index=True)
        combined = combined.drop_duplicates(subset=pk, keep='last')
        combined.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f'Upserted {len(new_df)} rows into {table_name} (table now {len(combined)} rows)')
        return len(new_df)
    except Exception:
        # table doesn't exist yet or read failed: create
        new_df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f'Created {table_name} with {len(new_df)} rows')
        return len(new_df)


def load_all():
    engine = create_conn()
    ensure_tables(engine)

    # load dim_taxpayer
    tp_csv = os.path.join(PROCESSED, 'taxpayers_clean.csv')
    upsert_csv_to_table(engine, tp_csv, 'dim_taxpayer', pk=['taxpayer_id'], parse_dates=['registration_date'])

    # load tax returns
    tr_csv = os.path.join(PROCESSED, 'tax_returns_clean.csv')
    upsert_csv_to_table(engine, tr_csv, 'fact_tax_returns', pk=['return_id'], parse_dates=['period_start','period_end','filing_date'])

    # load withholding
    wh_csv = os.path.join(PROCESSED, 'withholding_clean.csv')
    upsert_csv_to_table(engine, wh_csv, 'fact_withholding', pk=['withholding_id'], parse_dates=['date'])

    # load vat
    vat_csv = os.path.join(PROCESSED, 'vat_clean.csv')
    upsert_csv_to_table(engine, vat_csv, 'fact_vat', pk=['vat_id'], parse_dates=['date'])


def populate_dim_date(engine, min_date=None, max_date=None):
    """Populate dim_date table covering min_date..max_date (inclusive).
    If min/max not provided, derive from processed CSVs.
    """
    # try to derive from processed files
    dates = []
    candidates = [
        os.path.join(PROCESSED, 'tax_returns_clean.csv'),
        os.path.join(PROCESSED, 'vat_clean.csv'),
        os.path.join(PROCESSED, 'withholding_clean.csv')
    ]
    for fn in candidates:
        if os.path.exists(fn):
            try:
                df = pd.read_csv(fn, parse_dates=True)
                for col in df.columns:
                    if 'date' in col or 'period' in col:
                        try:
                            dseries = pd.to_datetime(df[col], errors='coerce')
                            dates.extend(dseries.dropna().dt.date.tolist())
                        except Exception:
                            pass
            except Exception:
                pass

    if dates:
        min_date = min(dates) if min_date is None else min_date
        max_date = max(dates) if max_date is None else max_date

    if min_date is None or max_date is None:
        print('No date range available to populate dim_date')
        return 0

    rng = pd.date_range(start=min_date, end=max_date)
    df_date = pd.DataFrame({
        'date': rng.date,
        'year': rng.year,
        'month': rng.month,
        'day': rng.day
    })
    df_date.to_sql('dim_date', engine, if_exists='replace', index=False)
    print(f'Populated dim_date with {len(df_date)} rows')
    return len(df_date)


def referential_integrity_check(engine):
    """Check for fact rows referencing missing taxpayers."""
    with engine.connect() as conn:
        res = conn.execute(text('''
            SELECT COUNT(*) FROM fact_tax_returns ft
            LEFT JOIN dim_taxpayer dt ON ft.taxpayer_id = dt.taxpayer_id
            WHERE dt.taxpayer_id IS NULL
        '''))
        missing_tr = res.scalar()
        res = conn.execute(text('''
            SELECT COUNT(*) FROM fact_withholding fw
            LEFT JOIN dim_taxpayer dt ON fw.taxpayer_id = dt.taxpayer_id
            WHERE dt.taxpayer_id IS NULL
        '''))
        missing_wh = res.scalar()
        res = conn.execute(text('''
            SELECT COUNT(*) FROM fact_vat fv
            LEFT JOIN dim_taxpayer dt ON fv.taxpayer_id = dt.taxpayer_id
            WHERE dt.taxpayer_id IS NULL
        '''))
        missing_vat = res.scalar()
    print('Referential integrity report:')
    print(' tax_returns missing taxpayers:', missing_tr)
    print(' withholding missing taxpayers:', missing_wh)
    print(' vat missing taxpayers:', missing_vat)
    return {'tax_returns': missing_tr, 'withholding': missing_wh, 'vat': missing_vat}


if __name__ == '__main__':
    load_all()
