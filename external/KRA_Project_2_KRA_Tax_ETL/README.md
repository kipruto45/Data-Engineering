# Project_2_KRA_Tax_ETL

Small end-to-end ETL project simulating KRA tax datasets.

Quick start

1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
```

2. Generate sample data (default 100k taxpayers):

```powershell
python scripts/generate_sample_data.py --size 100000
```

3. Run pipeline (extract -> transform -> load):

```powershell
python run_pipeline.py
```

Files of interest:
- `scripts/generate_sample_data.py` — generates robust raw CSVs
- `etl/extract/` — extract scripts
- `etl/transform/` — cleaning/transforms
- `etl/load/` — loaders including `load_to_sqlite.py`
- `kra_tax.db` — resulting SQLite warehouse

See `README_SETUP.md` for environment details and `config/dev_config.yaml` for paths and sizes.
