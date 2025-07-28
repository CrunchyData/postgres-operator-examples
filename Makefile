.PHONY: all clean test lint format
all clean test lint format:

SHELL := /bin/sh -e

venv:
	python -m venv venv
	. venv/bin/activate; \
	python -m pip install --upgrade pip

.PHONY: setup
setup: venv
	. venv/bin/activate; \
	pip install -r requirements/base.txt

.PHONY: install
install:
	pip install pre-commit;
	pre-commit install;

.PHONY: lint format
lint format:
ifdef CI
	pre-commit run --all-files --show-diff-on-failure
else
	pre-commit run --all-files || pre-commit run --all-files
endif

.PHONY: test
test:

.PHONY: clean
clean:
