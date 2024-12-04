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

build-docs:
	cd docs && pnpm docs:build

pre-commit-install:
	poetry run pre-commit install

format:
	poetry run ruff format --config pyproject.toml promptulate tests example
	poetry run ruff check --fix --config pyproject.toml promptulate tests example

test:
	$(TEST_COMMAND)

test-prod:
	$(TEST_COMMAND)
	poetry run coverage-badge -o docs/images/coverage.svg -f

check-codestyle:
	poetry run ruff format --check --config pyproject.toml promptulate tests example
	poetry run ruff check --config pyproject.toml promptulate tests example

check-format: check-codestyle

lint: check-codestyle test

# https://github.com/Maxlinn/linn-jupyter-site-template/blob/main/.github/workflows/linn-jupyter-site-template-deploy.yml
# Any notebook will be converted here.
# If there are any notebook will be changed, then the notebook will be converted to markdown and pushed to the repo.
build-docs:
	jupyter nbconvert ./example/chat_usage.ipynb --to markdown --output-dir ./docs/use_cases/
	jupyter nbconvert ./example/tools/custom_tool_usage.ipynb --to markdown --output-dir ./docs/modules/tools
	jupyter nbconvert ./example/llm/custom_llm.ipynb --to markdown --output-dir ./docs/modules/llm
	jupyter nbconvert ./example/llm/llm-factory-usage.ipynb --to markdown --output-dir ./docs/modules/llm
	jupyter nbconvert ./example/tools/langchain_tool_usage.ipynb --to markdown --output-dir ./docs/modules/tools
	jupyter nbconvert ./example/agent/assistant_agent_usage.ipynb --to markdown --output-dir ./docs/modules/agents
	jupyter nbconvert ./example/build-math-application-with-agent/build-math-application-with-agent.ipynb --to markdown --output-dir ./docs/use_cases/

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

.PHONY: lock install install-integration install-docs pre-commit-install polish-codestyle format check-format test test-prod lint build-docs start-docs pycache-remove dsstore-remove ipynbcheckpoints-remove pytestcache-remove build-remove cleanup help