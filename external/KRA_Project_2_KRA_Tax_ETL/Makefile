.PHONY: venv deps generate run test lint

venv:
	python -m venv .venv

deps:
	.venv\Scripts\Activate; pip install -r requirements.txt

generate:
	python scripts/generate_sample_data.py --size ${SIZE}

run:
	python run_pipeline.py

test:
	pytest -q

lint:
	black --check .
