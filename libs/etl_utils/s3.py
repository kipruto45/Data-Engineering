import os
from typing import Optional

import boto3


def upload_file_to_s3(local_path: str, bucket: str, key: str, region: Optional[str] = None):
    """Upload a file to S3 using boto3. Expects credentials to be available via environment or IAM role."""
    session = boto3.session.Session(region_name=region)
    s3 = session.client("s3")
    s3.upload_file(local_path, bucket, key)
    return f"s3://{bucket}/{key}"
