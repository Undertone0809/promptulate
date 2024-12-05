SHELL := /usr/bin/env bash
OS := $(shell python -c "import sys; print(sys.platform)")

ifeq ($(OS),win32)
	PYTHONPATH := $(shell python -c "import os; print(os.getcwd())")    
	TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests/basic
else
	PYTHONPATH := `pwd`
	TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests/basic
endif

lock:
	poetry lock -n && poetry export --without-hashes > requirements.txt

install:
	poetry install --with dev

install-integration:
	poetry install --with dev,test_integration

install-docs:
	cd docs && pnpm i

run-docs:
	cd docs && pnpm docs:dev

build-docs-prod:
	cd docs && pnpm docs:build

pre-commit-install:
	poetry run pre-commit install

format:
	poetry run ruff format --config pyproject.toml pne tests
	poetry run ruff check --fix --config pyproject.toml pne tests

test:
	$(TEST_COMMAND)

test-prod:
	$(TEST_COMMAND)
	poetry run coverage-badge -o docs/images/coverage.svg -f

check-codestyle:
	poetry run ruff format --check --config pyproject.toml pne
	poetry run ruff check --config pyproject.toml pne

check-format: check-codestyle

lint: check-codestyle test

help:
	@echo "lock: Lock the dependencies and export to requirements.txt"
	@echo "install: Install the dependencies"
	@echo "install-integration: Install the dependencies for integration testing"
	@echo "install-docs: Install the dependencies for building docs"
	@echo "pre-commit-install: Install the pre-commit hooks"
	@echo "polish-codestyle: Format the code"
	@echo "format: Format the code"
	@echo "check-format: Check the code format"
	@echo "check-codestyle: Check the code style, the same as make check-format"
	@echo "test: Run the tests"
	@echo "test-prod: Run the tests for production"
	@echo "lint: Run the tests and check the code style"
	@echo "build-docs: Build the docs"
	@echo "start-docs: Start the docs server"

.PHONY: lock install install-integration install-docs pre-commit-install polish-codestyle format check-format test test-prod lint build-docs start-docs pycache-remove dsstore-remove ipynbcheckpoints-remove pytestcache-remove build-remove cleanup help build-docs-prod