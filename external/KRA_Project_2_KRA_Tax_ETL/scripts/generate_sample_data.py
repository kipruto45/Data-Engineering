"""Generate sample KRA tax datasets. Writes CSVs into `data/raw/`.

Usage:
    python scripts/generate_sample_data.py --size 100000

This script uses Faker and numpy to create large, realistic synthetic datasets.
"""
import argparse
import csv
import os
import random
from datetime import datetime, timedelta

import numpy as np
from faker import Faker

fake = Faker()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')

os.makedirs(DATA_DIR, exist_ok=True)


def gen_taxpayers(n, path):
    fn = os.path.join(path, 'taxpayers_raw.csv')
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['taxpayer_id', 'name', 'pin', 'registration_date', 'sector', 'region'])
        for i in range(n):
            taxpayer_id = 1000000 + i
            name = fake.company()
            pin = 'PIN' + str(taxpayer_id)
            reg_date = fake.date_between(start_date='-10y', end_date='today').isoformat()
            sector = random.choice(['Agriculture','Manufacturing','Services','Trade','Others'])
            region = random.choice(['Nairobi','Mombasa','Kisumu','Nakuru','Eldoret'])
            writer.writerow([taxpayer_id, name, pin, reg_date, sector, region])
    return fn


def gen_tax_returns(n, taxpayers_n, path):
    fn = os.path.join(path, 'tax_returns_raw.csv')
    start = datetime(2018,1,1)
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['return_id','taxpayer_id','period_start','period_end','tax_due','tax_paid','filing_date'])
        for i in range(n):
            return_id = 2000000 + i
            tp = 1000000 + random.randint(0, taxpayers_n-1)
            start_date = start + timedelta(days=random.randint(0, 365*6))
            period_end = start_date + timedelta(days=30)
            tax_due = round(abs(np.random.normal(50000, 20000)),2)
            tax_paid = round(tax_due * random.choice([0.5,0.75,1.0,1.0,1.0,0.0]),2)
            filing = period_end + timedelta(days=random.randint(1,60))
            writer.writerow([return_id, tp, start_date.date().isoformat(), period_end.date().isoformat(), tax_due, tax_paid, filing.isoformat()])
    return fn


def gen_withholding(n, taxpayers_n, path):
    fn = os.path.join(path, 'withholding_raw.csv')
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['withholding_id','taxpayer_id','amount','date','payer'])
        for i in range(n):
            wid = 3000000 + i
            tp = 1000000 + random.randint(0, taxpayers_n-1)
            amount = round(abs(np.random.normal(2000, 1500)),2)
            date = fake.date_between(start_date='-3y', end_date='today').isoformat()
            payer = fake.company()
            writer.writerow([wid, tp, amount, date, payer])
    return fn


def gen_vat(n, taxpayers_n, path):
    fn = os.path.join(path, 'vat_raw.csv')
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['vat_id','taxpayer_id','transaction_value','vat_amount','date'])
        for i in range(n):
            vid = 4000000 + i
            tp = 1000000 + random.randint(0, taxpayers_n-1)
            tx = round(abs(np.random.normal(20000, 25000)),2)
            vat = round(tx * 0.16 * random.choice([0.8,1.0,1.0,1.2]),2)
            date = fake.date_between(start_date='-3y', end_date='today').isoformat()
            writer.writerow([vid, tp, tx, vat, date])
    return fn


def gen_penalties(n, taxpayers_n, path):
    fn = os.path.join(path, 'penalties_raw.csv')
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['penalty_id','taxpayer_id','amount','reason','date'])
        for i in range(n):
            pid = 5000000 + i
            tp = 1000000 + random.randint(0, taxpayers_n-1)
            amt = round(abs(np.random.exponential(2000)),2)
            reason = random.choice(['Late filing','Underpayment','Incorrect declaration','Other'])
            date = fake.date_between(start_date='-3y', end_date='today').isoformat()
            writer.writerow([pid, tp, amt, reason, date])
    return fn


def main(size):
    # size parameter refers to number of taxpayers; other datasets scale from that
    taxpayers_n = size
    print(f"Generating {taxpayers_n} taxpayers and related datasets in {DATA_DIR}")
    tfn = gen_taxpayers(taxpayers_n, DATA_DIR)
    gen_tax_returns(size * 12, taxpayers_n, DATA_DIR)  # monthly returns
    gen_withholding(size * 6, taxpayers_n, DATA_DIR)
    gen_vat(size * 20, taxpayers_n, DATA_DIR)
    gen_penalties(max(1000, int(size * 0.01)), taxpayers_n, DATA_DIR)
    print("Done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=100000, help='Number of taxpayers to generate')
    args = parser.parse_args()
    main(args.size)
