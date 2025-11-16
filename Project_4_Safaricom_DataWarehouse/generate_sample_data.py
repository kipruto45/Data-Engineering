"""Generate realistic warehouse ETL sample data for Project 4"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate 300 realistic transactions for warehouse loading
n_records = 300

# Kenyan phone numbers (254712-254799)
senders = [f'254{random.randint(712, 799)}{random.randint(100000, 999999):06d}' for _ in range(60)]
receivers = [f'254{random.randint(712, 799)}{random.randint(100000, 999999):06d}' for _ in range(60)]

# Transaction types
transaction_types = ['transfer', 'withdrawal', 'deposit', 'payment', 'airtime']
statuses = ['success', 'failed', 'pending', 'reversed']
providers = ['Safaricom', 'Airtel', 'Equity', 'KCB', 'Standard_Chartered']

# Generate data
data = []
base_time = datetime(2024, 1, 1)

for i in range(n_records):
    transaction_id = f'TXN{2024000001 + i}'
    sender = random.choice(senders)
    receiver = random.choice(receivers)
    
    # Amount: 100 to 100000 KES for warehouse analysis
    amount = np.random.lognormal(mean=9, sigma=1.8)
    amount = round(max(100, min(100000, amount)), 2)
    
    timestamp = base_time + timedelta(
        days=random.randint(0, 365),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    
    transaction_type = random.choice(transaction_types)
    
    # Status distribution: 75% success, 15% failed, 7% pending, 3% reversed
    rand = random.random()
    if rand < 0.75:
        status = 'success'
    elif rand < 0.90:
        status = 'failed'
    elif rand < 0.97:
        status = 'pending'
    else:
        status = 'reversed'
    
    fee = round(amount * 0.015, 2) if status == 'success' else 0
    
    data.append({
        'transaction_id': transaction_id,
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'fee': fee,
        'timestamp': timestamp.isoformat(),
        'transaction_date': timestamp.date(),
        'transaction_type': transaction_type,
        'status': status,
        'provider': random.choice(providers)
    })

# Create DataFrame
df = pd.DataFrame(data)

# Create data directory
os.makedirs('s3', exist_ok=True)

# Save as CSV (simulating S3 data)
df.to_csv('s3/warehouse_transactions_sample.csv', index=False)

# Also create a smaller export for PowerBI/dashboards
dashboard_df = df.groupby(['transaction_date', 'transaction_type', 'status']).agg({
    'amount': ['sum', 'mean', 'count'],
    'fee': 'sum'
}).reset_index()

os.makedirs('reports', exist_ok=True)
dashboard_df.to_csv('reports/transaction_summary.csv', index=False)

print(f'Generated {len(df)} warehouse transaction records')
print(f'Saved to: s3/warehouse_transactions_sample.csv')
print(f'Saved to: reports/transaction_summary.csv')
print(f'Date range: {df["transaction_date"].min()} to {df["transaction_date"].max()}')
print(f'Amount range: {df["amount"].min():.2f} to {df["amount"].max():.2f} KES')
print(f'Total transaction amount: {df[df["status"]=="success"]["amount"].sum():,.2f} KES')
print(f'Status distribution: {df["status"].value_counts().to_dict()}')
print(f'Transaction types: {df["transaction_type"].value_counts().to_dict()}')
print(f'Provider distribution: {df["provider"].value_counts().to_dict()}')
