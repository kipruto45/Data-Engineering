"""Generate realistic M-Pesa transaction sample data using transaction_generator module"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# Import the transaction generator
from generator.transaction_generator import TransactionGenerator

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Generate 500 realistic M-Pesa transactions using the module
generator = TransactionGenerator(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31)
)

# Generate transactions using the same module used in Airflow DAGs
transactions = generator.generate_transactions(count=500)

# Convert to DataFrame for CSV export
df = pd.DataFrame(transactions)

# Map generator status names to pipeline status names for consistency
status_mapping = {
    'success': 'completed',
    'failed': 'failed',
    'pending': 'pending',
    'reversed': 'failed'
}
df['status'] = df['status'].map(status_mapping)

# Add some realistic data quality issues (for testing data cleaning)
# This tests the robustness of the cleaning pipeline

# Add some nulls (2% - simulate real data quality issues)
null_indices = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
for idx in null_indices:
    df.loc[idx, np.random.choice(['amount', 'status'])] = None

# Add some duplicates (5 - simulate real duplicate transactions)
dup_indices = np.random.choice(df.index, size=5, replace=False)
for idx in dup_indices:
    df = pd.concat([df, df.loc[[idx]]], ignore_index=True)

# Select relevant columns for M-Pesa pipeline
columns = ['transaction_id', 'sender', 'receiver', 'amount', 'fee', 'timestamp', 'transaction_type', 'status']
df = df[columns]

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
