IMAGE_NAME ?= mlops-app-crunchy-postgres
IMAGE_TAG ?= latest

.PHONY: all clean test lint format
all clean test lint format:

SHELL := /bin/sh -e

.PHONY: install setup
install setup: poetry.lock
	poetry config virtualenvs.in-project true
	poetry install --with dev
	poetry run pre-commit install;

.PHONY: install
install:
	poetry config virtualenvs.in-project true
	poetry install --with dev
	poetry run pre-commit install;

.PHONY: format
format:
ifdef CI
	poetry run pre-commit run --all-files --show-diff-on-failure
else
	# automatically fix the formatting issues and rerun again
	poetry run pre-commit run --all-files || poetry run pre-commit run --all-files
endif

.PHONY: lint
lint: format
	poetry run mypy .apolo

.PHONY: test-unit
test-unit:
	poetry run pytest -vvs --cov=.apolo --cov-report xml:.coverage.unit.xml .apolo/tests/unit

.PHONY: test-integration
test-integration:
	poetry run pytest -vv --cov=.apolo --cov-report xml:.coverage.integration.xml .apolo/tests/integration

.PHONY: build-hook-image
build-hook-image:
	docker build \
		-t $(IMAGE_NAME):latest \
		-f hooks.Dockerfile \
		.;

.PHONY: push-hook-image
push-hook-image:
	docker tag $(IMAGE_NAME):latest ghcr.io/neuro-inc/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push ghcr.io/neuro-inc/$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: gen-types-schemas
gen-types-schemas:
	app-types dump-types-schema .apolo/src/apolo_apps_postgresql PostgresInputs .apolo/src/apolo_apps_postgresql/schemas/PostgresInputs.json
	app-types dump-types-schema .apolo/src/apolo_apps_postgresql PostgresOutputs .apolo/src/apolo_apps_postgresql/schemas/PostgresOutputs.json
