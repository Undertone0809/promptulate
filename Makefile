#* Poetry
.PHONY: poetry-download
poetry-download:
	pip install poetry

#* Installation
.PHONY: install
install:
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install -n

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

#* Formatters
.PHONY: polish-codestyle
polish-codestyle:
	poetry run isort --settings-path pyproject.toml promptulate tests example
	poetry run black --config pyproject.toml promptulate tests example

.PHONY: formatting
formatting: polish-codestyle

#* Linting
.PHONY: test
test:
	poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate ./tests/test_chat.py ./tests/output_formatter

.PHONY: check-codestyle
check-codestyle:
	poetry run isort --diff --check-only --settings-path pyproject.toml promptulate tests example
	poetry run black --diff --check --config pyproject.toml promptulate tests example

.PHONY: check-safety
check-safety:
	poetry check
	poetry run safety check --full-report
	poetry run bandit -ll --recursive hooks

.PHONY: lint
lint: test check-codestyle

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove ipynbcheckpoints-remove pytestcache-remove
