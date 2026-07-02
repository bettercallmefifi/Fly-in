MAP ?= map

venv:
	python3 -m venv venv

install:
	pip install -r requirements.txt

run:
	python3 src/main.py $(MAP)

debug:
	python3 -m pdb src/main.py $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 src/
	mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 src/
	mypy src/ --strict

.PHONY: run clean lint lint-strict debug install