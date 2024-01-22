SHELL := /usr/bin/env bash
OS := $(shell python -c "import sys; print(sys.platform)")

# all test files define here
DEV_TEST_TOOL_FILES := ./tests/tools/test_human_feedback_tool.py ./tests/tools/test_calculator.py ./tests/tools/test_python_repl_tools.py ./tests/tools/test_sleep_tool.py
DEV_TEST_HOOK_FILES := ./tests/hook/test_llm.py ./tests/hook/test_tool_hook.py
DEV_TEST_LLM_FILES := ./tests/llms/test_openai.py
DEV_TEST_FILES := $(DEV_TEST_TOOL_FILES) $(DEV_TEST_HOOK_FILES) $(DEV_TEST_LLM_FILES) ./tests/test_chat.py ./tests/output_formatter ./tests/test_import.py ./tests/utils/test_string_template.py

ifeq ($(OS),win32)
	PYTHONPATH := $(shell python -c "import os; print(os.getcwd())")
    TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate $(DEV_TEST_FILES)
	TEST_PROD_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests
else
	PYTHONPATH := `pwd`
    TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate $(DEV_TEST_FILES)
	TEST_PROD_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests
endif

.PHONY: lock
lock:
	poetry lock -n && poetry export --without-hashes > requirements.txt

.PHONY: install
install:
	poetry install --with dev

.PHONY: install-integration
install-integration:
	poetry install --with dev,test_integration

.PHONY: install-docs
install-docs:
	npm i docsify-cli -g

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

.PHONY: polish-codestyle
polish-codestyle:
	poetry run ruff format --config pyproject.toml promptulate tests example
	poetry run ruff check --fix --config pyproject.toml promptulate tests example

.PHONY: formatting
formatting: polish-codestyle

.PHONY: test
test:
	$(TEST_COMMAND)

.PHONY: test-prod
test-prod:
	$(TEST_PROD_COMMAND)
	poetry run coverage-badge -o docs/images/coverage.svg -f

.PHONY: check-codestyle
check-codestyle:
	poetry run ruff format --check --config pyproject.toml promptulate tests example
	poetry run ruff check --config pyproject.toml promptulate tests example

.PHONY: lint
lint: check-codestyle test

# https://github.com/Maxlinn/linn-jupyter-site-template/blob/main/.github/workflows/linn-jupyter-site-template-deploy.yml
# Any notebook will be converted here.
# If there are any notebook will be changed, then the notebook will be converted to markdown and pushed to the repo.
.PHONY: build-docs
build-docs:
	jupyter nbconvert ./example/chat_usage.ipynb --to markdown --output-dir ./docs/uses_cases/
	jupyter nbconvert ./example/tools/custom_tool_usage.ipynb --to markdown --output-dir ./docs/modules/tools
	jupyter nbconvert ./example/llm/custom_llm.ipynb --to markdown --output-dir ./docs/modules/llm

.PHONY: start-docs
start-docs:
	docsify serve docs

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
