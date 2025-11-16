"""Generate realistic Kafka streaming data sample for Project 3"""

import pandas as pd
import numpy as np
import json
import os
import uuid
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate 200 realistic M-Pesa transactions for streaming
n_records = 200

# Kenyan phone numbers (254712-254799)
senders = [f'254{random.randint(712, 799)}{random.randint(100000, 999999):06d}' for _ in range(50)]
receivers = [f'254{random.randint(712, 799)}{random.randint(100000, 999999):06d}' for _ in range(50)]

# Transaction types
transaction_types = ['transfer', 'withdrawal', 'deposit', 'payment']
statuses = ['success', 'failed', 'pending']
providers = ['Safaricom', 'Airtel', 'Equity']

# Generate data
data = []
base_time = datetime(2024, 6, 1)

for i in range(n_records):
    transaction_id = f'TXN{str(uuid.uuid4())[:8].upper()}'
    sender = random.choice(senders)
    receiver = random.choice(receivers)
    
    # Amount: 100 to 50000 KES
    amount = round(random.uniform(100, 50000), 2)
    
    timestamp = base_time + timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    
    transaction_type = random.choice(transaction_types)
    
    # Status weighted towards success
    rand = random.random()
    if rand < 0.85:
        status = 'success'
    elif rand < 0.93:
        status = 'failed'
    else:
        status = 'pending'
    
    fee = round(amount * 0.01, 2) if status == 'success' else 0
    
    data.append({
        'transaction_id': transaction_id,
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'fee': fee,
        'timestamp': timestamp.isoformat(),
        'transaction_type': transaction_type,
        'status': status,
        'provider': random.choice(providers)
    })

# Create DataFrame
df = pd.DataFrame(data)

# Create data directory
os.makedirs('data', exist_ok=True)

# Save to JSON (typical for Kafka streaming)
with open('data/sample_kafka_transactions.json', 'w') as f:
    for record in data:
        f.write(json.dumps(record) + '\n')

# Also save as CSV for reference
df.to_csv('data/sample_kafka_transactions.csv', index=False)

print(f'Generated {len(df)} Kafka streaming transactions')
print(f'Saved to: data/sample_kafka_transactions.json (JSONL format)')
print(f'Saved to: data/sample_kafka_transactions.csv')
print(f'Date range: {df["timestamp"].min()} to {df["timestamp"].max()}')
print(f'Amount range: {df["amount"].min():.2f} to {df["amount"].max():.2f} KES')
print(f'Status distribution: {df["status"].value_counts().to_dict()}')
print(f'Transaction types: {df["transaction_type"].value_counts().to_dict()}')
