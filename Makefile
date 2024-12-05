.PHONY: lock install lint format run-docs build-docs

help:
	@echo "lock: Lock the dependencies and export to requirements.txt"
	@echo "install: Install the dependencies"
	@echo "lint: Lint the code"
	@echo "format: Format the code"
	@echo "run-docs: Run the documentation"
	@echo "build-docs: Build the documentation"

lock:
	poetry lock -n && poetry export --without-hashes > requirements.txt

install:
	poetry install --with dev

lint:
	poetry run ruff check libs

format:
	poetry run ruff format libs

run-docs:
	cd docs && pnpm docs:dev

build-docs:
	cd docs && pnpm docs:build