"""Generate realistic M-Pesa transaction sample data"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate 500 realistic M-Pesa transactions
n_records = 500

# Kenyan phone numbers (254712-254799)
senders = [f'254{random.randint(712, 799)}{random.randint(100000, 999999):06d}' for _ in range(100)]
receivers = [f'254{random.randint(712, 799)}{random.randint(100000, 999999):06d}' for _ in range(100)]

# Transaction types
transaction_types = ['Transfer', 'Withdrawal', 'Deposit', 'Payment', 'Reversal']
statuses = ['completed', 'pending', 'failed']

# Generate data
data = []
base_time = datetime(2024, 1, 1)

for i in range(n_records):
    transaction_id = f'TXN{2024000001 + i}'
    sender = random.choice(senders)
    receiver = random.choice(receivers)
    
    # Amount: 100 to 50000 KES with more small transactions
    amount = np.random.lognormal(mean=8, sigma=1.5)
    amount = round(max(100, min(50000, amount)), 2)
    
    timestamp = base_time + timedelta(
        days=random.randint(0, 365),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    
    transaction_type = random.choice(transaction_types)
    
    # Status weighted towards completed
    rand = random.random()
    if rand < 0.90:
        status = 'completed'
    elif rand < 0.95:
        status = 'pending'
    else:
        status = 'failed'
    
    fee = round(amount * 0.01, 2) if status == 'completed' else 0
    
    data.append({
        'transaction_id': transaction_id,
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'fee': fee,
        'timestamp': timestamp.isoformat(),
        'transaction_type': transaction_type,
        'status': status
    })

# Create DataFrame
df = pd.DataFrame(data)

# Add some realistic data quality issues (for testing data cleaning)
# Add some nulls (2%)
null_indices = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
for idx in null_indices:
    df.loc[idx, random.choice(['amount', 'status'])] = None

# Add some duplicates (5)
dup_indices = np.random.choice(df.index, size=5, replace=False)
for idx in dup_indices:
    df = pd.concat([df, df.loc[[idx]]], ignore_index=True)

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Save to CSV
df.to_csv('data/sample_mpesa_transactions.csv', index=False)

print(f'Generated {len(df)} M-Pesa transactions')
print(f'Saved to: data/sample_mpesa_transactions.csv')
print(f'Columns: {list(df.columns)}')
print(f'Date range: {df["timestamp"].min()} to {df["timestamp"].max()}')
print(f'Amount range: {df["amount"].min():.2f} to {df["amount"].max():.2f} KES')
print(f'Null values: {int(df.isnull().sum().sum())}')
print(f'Duplicate transactions: {df["transaction_id"].duplicated().sum()}')
print(f'Transaction types: {df["transaction_type"].value_counts().to_dict()}')
print(f'Status distribution: {df["status"].value_counts().to_dict()}')
