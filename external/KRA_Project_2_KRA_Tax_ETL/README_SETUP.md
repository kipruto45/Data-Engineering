Setup
-----

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate
pip install -r requirements.txt
```

2. (Optional) Copy `.env.example` to `.env` and adjust values.

3. Generate sample data (pick a size appropriate for your machine):

```powershell
# 100k taxpayers (default):
python scripts/generate_sample_data.py --size 100000

# For a very large dataset (e.g., 1 million taxpayers), ensure you have enough disk and memory:
python scripts/generate_sample_data.py --size 1000000
```

4. Run pipeline (extract -> transform -> load):

```powershell
python run_pipeline.py
```

Notes
-----
- `scripts/generate_sample_data.py` writes CSVs to `data/raw/` and scales related datasets from the taxpayer `--size` argument.
- `run_pipeline.py` currently demonstrates taxpayers extraction, cleaning and loading to `kra_tax.db`. Expand ETL for other files by following the same pattern.
- To export for PowerBI, run `python scripts/export_for_powerbi.py` after the DB is populated.
