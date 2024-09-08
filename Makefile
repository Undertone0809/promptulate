SHELL := /usr/bin/env bash
OS := $(shell python -c "import sys; print(sys.platform)")

# all test files define here
DEV_TEST_TOOL_FILES := ./tests/tools/test_human_feedback_tool.py ./tests/tools/test_calculator.py ./tests/tools/test_python_repl_tools.py ./tests/tools/test_sleep_tool.py ./tests/tools/test_arxiv_tools.py ./tests/tools/test_tool_manager.py ./tests/tools/test_file_tools.py
DEV_TEST_HOOK_FILES := ./tests/hook/test_llm.py ./tests/hook/test_tool_hook.py
DEV_TEST_LLM_FILES := ./tests/llms/test_openai.py ./tests/llms/test_factory.py
DEV_TEST_AGENT_FILES := ./tests/agents/test_tool_agent.py ./tests/agents/test_assistant_agent.py
DEV_TEST_BETA := ./tests/beta/test_st.py
DEV_TEST_FILES := $(DEV_TEST_BETA) $(DEV_TEST_TOOL_FILES) $(DEV_TEST_HOOK_FILES) $(DEV_TEST_LLM_FILES) $(DEV_TEST_AGENT_FILES) ./tests/test_chat.py ./tests/output_formatter ./tests/test_import.py ./tests/utils/test_string_template.py 


ifeq ($(OS),win32)
	PYTHONPATH := $(shell python -c "import os; print(os.getcwd())")
    # TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate $(DEV_TEST_FILES)
	TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests/basic
	TEST_PROD_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests
else
	PYTHONPATH := `pwd`
    # TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate $(DEV_TEST_FILES)
	TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests/basic
	TEST_PROD_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=promptulate tests
endif

lock:
	poetry lock -n && poetry export --without-hashes > requirements.txt

install:
	poetry install --with dev

install-integration:
	poetry install --with dev,test_integration

install-docs:
	cd docs && pnpm i

build-docs-prod:
	cd docs && pnpm docs:build

pre-commit-install:
	poetry run pre-commit install

format:
	poetry run ruff format --config pyproject.toml promptulate tests example
	poetry run ruff check --fix --config pyproject.toml promptulate tests example

test:
	$(TEST_COMMAND)

test-prod:
	$(TEST_PROD_COMMAND)
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


start-docs:
	cd docs && npm run docs:dev

#* Cleaning
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

build-remove:
	rm -rf build/

cleanup: pycache-remove dsstore-remove ipynbcheckpoints-remove pytestcache-remove

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
	@echo "pycache-remove: Remove the pycache"
	@echo "dsstore-remove: Remove the .DS_Store files"
	@echo "ipynbcheckpoints-remove: Remove the ipynb checkpoints"
	@echo "pytestcache-remove: Remove the pytest cache"
	@echo "build-remove: Remove the build directory"
	@echo "cleanup: Remove all the cache files"

.PHONY: lock install install-integration install-docs pre-commit-install polish-codestyle formatting format test test-prod check-codestyle lint build-docs start-docs pycache-remove dsstore-remove ipynbcheckpoints-remove pytestcache-remove build-remove cleanup help check-format