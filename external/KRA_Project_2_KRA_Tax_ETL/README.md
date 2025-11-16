````markdown
# Project 2 — KRA Tax ETL

This is an end-to-end sample ETL project that simulates Kenyan Revenue Authority (KRA) datasets and demonstrates a robust local ETL workflow:

- Generate large synthetic datasets (taxpayers, tax returns, VAT, withholding, penalties)
- Extract CSVs, perform lightweight cleaning/transforms, and load into a local SQLite warehouse (`kra_tax.db`)
- Support for idempotent/upsert and incremental loads for large fact tables
- Optional helpers to upload processed CSVs to S3 and produce Redshift COPY commands

This README explains how the project is organized and how to run each part so other developers can understand and use it.

**Project Layout**
- `config/`: `dev_config.yaml`, `prod_config.yaml`, `logging.conf`
- `data/raw/`: generated raw CSVs (taxpayers_raw.csv, tax_returns_raw.csv, vat_raw.csv, withholding_raw.csv, penalties_raw.csv)
- `data/processed/`: extracted & cleaned CSVs used for loading into the warehouse
- `data/warehouse/`: CSV snapshots of warehouse exports
- `etl/extract/`: extract scripts that read `data/raw` and write extracted CSVs into `data/processed`
- `etl/transform/`: cleaning functions for each source
- `etl/load/`: loaders: `load_to_sqlite.py`, `load_to_s3.py`, `load_to_redshift.py` (placeholder)
- `scripts/`:
  - `generate_sample_data.py` — synthetic data generator (size configurable)
  - `sync_to_s3.py` — upload processed CSVs and print Redshift COPY commands
  - `export_for_powerbi.py` — export tables for PowerBI
- `run_pipeline.py`: orchestrator (optional `--generate --size`) that runs extract -> transform -> load
- `requirements.txt`: Python dependencies
- `kra_tax.db`: local SQLite warehouse (created/updated by the pipeline)

## How it works — high level

1. Data generation
	- `scripts/generate_sample_data.py --size N` creates `N` taxpayers and scales related tables proportionally (tax returns, VAT, withholding, penalties).

2. Extract
	- `etl/extract/*.py` read raw CSVs and write consistent extracted CSVs into `data/processed`.

3. Transform / Clean
	- `etl/transform/*.py` perform lightweight cleaning: parse dates, coerce numeric columns, fill nulls, basic normalization.

4. Load
	- `etl/load/load_to_sqlite.py`:
	  - Creates dimensional & fact tables if they don't exist (`dim_taxpayer`, `dim_date`, `fact_tax_returns`, `fact_withholding`, `fact_vat`).
	  - Upserts `dim_taxpayer` to avoid duplicates.
	  - Performs incremental chunked appends for large fact tables by comparing the CSV primary-key values against the existing max PK in the DB (memory-friendly).
	  - Provides helpers to populate `dim_date` and run referential integrity checks.

5. Optional: S3 / Redshift
	- `scripts/sync_to_s3.py` uploads processed CSVs to an S3 bucket and prints sample Redshift COPY commands. Use `etl/load/load_to_s3.py` to upload programmatically.

## Quick Start (Windows PowerShell)

1) Create a virtual environment and install dependencies

```powershell
cd d:/Project/KRA/Project_2_KRA_Tax_ETL
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

2) Generate sample data (example sizes)

```powershell
# Small quick run
python scripts/generate_sample_data.py --size 100

# Medium: 100k taxpayers (realistic scale — requires disk & CPU)
python scripts/generate_sample_data.py --size 100000

# Very large (1M) — ensure you have resources
python scripts/generate_sample_data.py --size 1000000
```

3) Run the full ETL pipeline (optional generation step)

```powershell
# Generate then run pipeline
python run_pipeline.py --generate --size 100000

# Or run pipeline using existing raw CSVs
python run_pipeline.py
```

4) Export for PowerBI (optional)

```powershell
python scripts/export_for_powerbi.py
```

5) Upload processed CSVs to S3 for Redshift (optional)

```powershell
python scripts/sync_to_s3.py --bucket my-bucket --prefix kra/processed --region us-east-1
```

## Testing

There is a basic test that generates a small dataset and runs the pipeline:

```powershell
pytest tests/test_generate_and_load.py -q
```

Use small sizes in CI to keep runs fast.

## Git LFS and Large Files

Large generated CSVs were migrated into Git LFS for this repository on 2025-11-16. See `../LFS_MIGRATION.md` in the repository root for details and steps to update local clones.

Recommendations:
- For production or large-scale experiments, keep generated data outside the Git repository (S3 is recommended). Use `sync_to_s3.py` to upload processed artifacts.
- If you clone the repo and encounter missing large files, install Git LFS and run `git lfs pull` in the repository.

## Implementation notes & design choices

- Synthetic data: uses `Faker` and `numpy` to produce realistic, varied values.
- Scaling: generator scales the number of returns, VAT, and withholding records relative to the taxpayer count so you can produce realistic volumes.
- Memory safety: incremental loads read CSVs in chunks and append only rows with PK > current max PK in the DB.
- Upserts: `dim_taxpayer` is upserted to keep the dimension idempotent.
- Referential checks: `load_to_sqlite.py` exposes `referential_integrity_check()` to detect any fact rows with missing dimension keys.

## Troubleshooting

- If `run_pipeline.py` fails with SQLAlchemy `ObjectNotExecutableError`, ensure the `etl/load/load_to_sqlite.py` uses `sqlalchemy.text()` for raw SQL execution. The project includes that fix.
- If the pipeline is slow for very large datasets, increase `chunksize` in `incremental_load_csv()` or run the generator on a machine with faster I/O.
- If you see `git` warnings about large files after cloning, run:

```powershell
git lfs install
git lfs pull
```

## Next steps and improvements

- Add production connectors (Redshift loader implementation, IAM role automation).
- Add CI pipeline that runs the generator with `--size 1000` and validates the ETL end-to-end.
- Add data quality checks (row counts, null thresholds, distribution checks) and alerting.

## Contact / Maintainers

If you need help, open an issue in the main repository or contact the repository owner.

---

This README aims to make it trivial for new contributors or reviewers to understand how to run and extend the ETL project.

````
