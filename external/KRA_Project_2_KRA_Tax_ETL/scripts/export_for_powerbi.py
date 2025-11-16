"""Export warehouse tables to CSVs for PowerBI."""
import os
import pandas as pd
from sqlalchemy import create_engine

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB = os.path.join(BASE, 'kra_tax.db')
OUT = os.path.join(BASE, 'dashboards')

os.makedirs(OUT, exist_ok=True)


def export_table(table, out_name=None):
    engine = create_engine(f'sqlite:///{DB}')
    df = pd.read_sql_table(table, engine)
    of = os.path.join(OUT, out_name or f'{table}.csv')
    df.to_csv(of, index=False)
    print('Exported', table, '->', of)


if __name__ == '__main__':
    # best-effort exports
    for t in ['dim_taxpayer']:
        try:
            export_table(t, t + '.csv')
        except Exception as e:
            print('Skipping', t, e)
