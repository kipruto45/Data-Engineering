"""Simple S3 uploader for CSVs. Requires `boto3` configured with credentials.
This is a helper used optionally after loading to the warehouse.
"""
import os
import boto3
from botocore.exceptions import ClientError


def upload_file(file_path: str, bucket: str, key: str, region: str = 'us-east-1') -> bool:
    s3 = boto3.client('s3', region_name=region)
    try:
        s3.upload_file(file_path, bucket, key)
        print(f'Uploaded {file_path} to s3://{bucket}/{key}')
        return True
    except ClientError as e:
        print('S3 upload failed:', e)
        return False
