# Contributing

Thank you for contributing to Project_2_KRA_Tax_ETL. This document explains how to run, test and contribute.

Developer setup

```powershell
cd external/KRA_Project_2_KRA_Tax_ETL
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

Pre-commit hooks

```powershell
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Running locally

```powershell
# generate sample data
make generate SIZE=1000

# run pipeline
make run
```

CI and automation

- A scheduled workflow runs the pipeline daily and on push to `main` (see `.github/workflows/etl_run.yml`).
- PRs run lint and tests through `.github/workflows/ci.yml`.

Large data

- Large generated CSVs are stored in S3 for releases; DO NOT commit large generated data to the repository main branch. See `../LFS_MIGRATION.md` for the previous migration.