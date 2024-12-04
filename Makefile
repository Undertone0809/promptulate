.PHONY: lock install

help:
	@echo "lock: Lock the dependencies and export to requirements.txt"
	@echo "install: Install the dependencies"

lock:
	poetry lock -n && poetry export --without-hashes > requirements.txt

install:
	poetry install --with dev

lint:
	poetry run ruff check libs
