SHELL := /usr/bin/env bash
OS := $(shell python -c "import sys; print(sys.platform)")

ifeq ($(OS),win32)
	PYTHONPATH := $(shell python -c "import os; print(os.getcwd())")
    TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate ./tests/test_chat.py ./tests/output_formatter
	TEST_PROD_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests
else
	PYTHONPATH := `pwd`
    TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate ./tests/test_chat.py ./tests/output_formatter
	TEST_PROD_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests
endif


#* Installation
.PHONY: install
install:
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install --with dev

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

#* Formatters
.PHONY: polish-codestyle
polish-codestyle:
	poetry run ruff format --config pyproject.toml promptulate tests example
	poetry run ruff check --fix --config pyproject.toml promptulate tests example

.PHONY: formatting
formatting: polish-codestyle

#* Linting
.PHONY: test
test:
	$(TEST_COMMAND)
	poetry run coverage-badge -o docs/images/coverage.svg -f

#* Linting
.PHONY: test-prod
test-prod:
	$(TEST_PROD_COMMAND)
	poetry run coverage-badge -o docs/images/coverage.svg -f

.PHONY: check-codestyle
check-codestyle:
	poetry run ruff format --check --config pyproject.toml promptulate tests example
	poetry run ruff check --config pyproject.toml promptulate tests example

.PHONY: lint
lint: test check-codestyle

#* https://github.com/Maxlinn/linn-jupyter-site-template/blob/main/.github/workflows/linn-jupyter-site-template-deploy.yml
.PHONY: build-docs
build-docs:
	jupyter nbconvert ./docs/modules/chat_usage.ipynb --to markdown

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
