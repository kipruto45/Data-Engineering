"""Orchestrator: generate (optional) -> extract -> transform -> load for all datasets."""
import argparse
import logging
import os
import subprocess

from etl.extract import extract_taxpayers, extract_tax_returns, extract_vat, extract_withholding
from etl.transform import clean_taxpayers, clean_tax_returns, clean_vat, clean_withholding
from etl.load import load_to_sqlite

logging.basicConfig(level=logging.INFO)

BASE = os.path.abspath(os.path.dirname(__file__))
SCRIPTS = os.path.join(BASE, 'scripts')


def run_extract_transform_load():
    # Extract
    logging.info('Extracting datasets')
    df_tp = extract_taxpayers.extract_taxpayers()
    df_tr = extract_tax_returns.extract_tax_returns()
    df_vat = extract_vat.extract_vat()
    df_wh = extract_withholding.extract_withholding()

    # Transform/clean
    logging.info('Cleaning datasets')
    df_tp = clean_taxpayers.clean_taxpayers(df_tp)
    df_tr = clean_tax_returns.clean_tax_returns(df_tr)
    df_vat = clean_vat.clean_vat(df_vat)
    df_wh = clean_withholding.clean_withholding(df_wh)

    # write cleaned
    processed = os.path.join(BASE, 'data', 'processed')
    os.makedirs(processed, exist_ok=True)
    df_tp.to_csv(os.path.join(processed, 'taxpayers_clean.csv'), index=False)
    df_tr.to_csv(os.path.join(processed, 'tax_returns_clean.csv'), index=False)
    df_vat.to_csv(os.path.join(processed, 'vat_clean.csv'), index=False)
    df_wh.to_csv(os.path.join(processed, 'withholding_clean.csv'), index=False)

    # Load
    logging.info('Loading into SQLite')
    load_to_sqlite.load_all()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true', help='Run data generator before pipeline')
    parser.add_argument('--size', type=int, default=1000, help='If generating, size parameter (taxpayers)')
    args = parser.parse_args()

    if args.generate:
        cmd = ['python', os.path.join(SCRIPTS, 'generate_sample_data.py'), '--size', str(args.size)]
        logging.info('Generating sample data: %s', ' '.join(cmd))
        subprocess.check_call(cmd)

    run_extract_transform_load()
