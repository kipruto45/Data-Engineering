from pathlib import Path
import os
import subprocess
from typing import Optional

from prefect import flow, task, get_run_logger


@task
def generate_data(size: int = 1000) -> Path:
    logger = get_run_logger()
    project_root = Path(__file__).resolve().parents[2]
    script = project_root / "scripts" / "generate_sample_data.py"
    logger.info(f"Generating data with size={size} using {script}")
    subprocess.check_call(["python", str(script), "--size", str(size)])
    return project_root / "data" / "raw"


@task
def run_pipeline() -> None:
    logger = get_run_logger()
    project_root = Path(__file__).resolve().parents[2]
    entry = project_root / "run_pipeline.py"
    logger.info(f"Running pipeline: {entry}")
    subprocess.check_call(["python", str(entry)])


@task
def run_dq_and_optional_upload(s3_bucket: Optional[str] = None, s3_prefix: Optional[str] = "kra/processed") -> dict:
    logger = get_run_logger()
    # import lazily to avoid requiring DB libs at import time
    from etl.load.load_to_sqlite import create_conn
    from etl.quality import basic_checks
    from etl.load import load_to_s3

    engine = create_conn("kra_tax.db")
    ok, details = basic_checks(engine)
    logger.info(f"DQ OK: {ok} -- {details}")

    s3_results = {}
    if s3_bucket and ok:
        # upload small processed CSVs found in data/processed
        project_root = Path(__file__).resolve().parents[2]
        processed = project_root / "data" / "processed"
        for f in processed.glob("*.csv"):
            key = f"{s3_prefix.rstrip('/')}/{f.name}"
            logger.info(f"Uploading {f} to s3://{s3_bucket}/{key}")
            success = load_to_s3.upload_file(str(f), s3_bucket, key, region=os.getenv("AWS_REGION", "us-east-1"))
            s3_results[f.name] = success

    return {"dq_ok": ok, "dq_details": details, "s3_uploads": s3_results}


@flow(name="KRA ETL Flow")
def kra_etl_flow(generate: bool = True, size: int = 1000, s3_bucket: Optional[str] = None, s3_prefix: Optional[str] = "kra/processed"):
    logger = get_run_logger()
    if generate:
        generate_data(size)
    run_pipeline()
    res = run_dq_and_optional_upload(s3_bucket=s3_bucket, s3_prefix=s3_prefix)
    logger.info("Flow finished")
    return res


if __name__ == "__main__":
    # allow overriding via environment variables when run in CI
    gen = os.getenv("KRA_GENERATE", "true").lower() in ("1", "true", "yes")
    size = int(os.getenv("KRA_SIZE", "1000"))
    s3_bucket = os.getenv("S3_BUCKET")
    s3_prefix = os.getenv("S3_PREFIX", "kra/processed")
    kra_etl_flow(generate=gen, size=size, s3_bucket=s3_bucket, s3_prefix=s3_prefix)
