.PHONY: help all setup sync install pkg-install pkg-test pkg-lint pkg-format pkg-build pkg-build-pne pkg-build-cli docs-install docs-dev docs-build docs-preview docs-clean clean

SHELL := /bin/zsh
UV := uv
NPM := npm
PYTHON := python

PACKAGE_DIRS := packages/pne packages/pne-cli
DOCS_DIR := docs

help:
	@echo "Available targets:"
	@echo "  make setup            - Install Python + docs dependencies."
	@echo "  make sync             - Sync workspace dependencies (alias for uv sync)."
	@echo "  make install           - Alias for pkg-install."
	@echo "  make pkg-install       - Sync workspace dependencies."
	@echo "  make pkg-test          - Run python tests via unittest."
	@echo "  make pkg-lint          - Run Ruff check."
	@echo "  make pkg-format        - Run Ruff format."
	@echo "  make pkg-build         - Build all packages."
	@echo "  make pkg-build-pne     - Build packages/pne."
	@echo "  make pkg-build-cli     - Build packages/pne-cli."
	@echo "  make docs-install      - Install docs dependencies."
	@echo "  make docs-dev          - Run docs dev server."
	@echo "  make docs-build        - Build docs site."
	@echo "  make docs-preview      - Preview built docs."
	@echo "  make docs-clean        - Remove docs build artifacts."
	@echo "  make clean             - Remove local build artifacts."

all: help

setup: sync docs-install

sync:
	$(UV) sync

install: pkg-install

pkg-install: sync

pkg-test:
	$(UV) run $(PYTHON) -m unittest

pkg-lint:
	$(UV) run ruff check .

pkg-format:
	$(UV) run ruff format .

pkg-build: pkg-build-pne pkg-build-cli

pkg-build-pne:
	cd $(firstword $(PACKAGE_DIRS)) && $(UV) build

pkg-build-cli:
	cd $(word 2,$(PACKAGE_DIRS)) && $(UV) build

docs-install:
	cd $(DOCS_DIR) && $(NPM) install

docs-dev:
	cd $(DOCS_DIR) && $(NPM) run docs:dev

docs-build:
	cd $(DOCS_DIR) && $(NPM) run docs:build

docs-preview:
	cd $(DOCS_DIR) && $(NPM) run docs:preview

docs-clean:
	rm -rf $(DOCS_DIR)/.vitepress/dist

clean:
	rm -rf $(foreach pkg,$(PACKAGE_DIRS),$(pkg)/dist) \
		$(DOCS_DIR)/.vitepress/.temp $(DOCS_DIR)/.vitepress/dist $(DOCS_DIR)/node_modules

