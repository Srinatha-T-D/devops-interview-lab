PYTHON ?= python
IMAGE ?= order-api:local
TEST_IMAGE ?= order-api:test

.PHONY: help install lint format-check test test-docker check check-docker up down logs status build incident

help:
	@echo "install       Install application and developer dependencies"
	@echo "lint          Run static analysis"
	@echo "format-check  Verify source formatting"
	@echo "test          Run fast unit tests"
	@echo "test-docker   Run lint, format, and unit tests in Docker"
	@echo "check         Run all local quality gates"
	@echo "check-docker  Run all quality gates without a local Python install"

install:
	$(PYTHON) -m pip install -r requirements-dev.txt

lint:
	$(PYTHON) -m ruff check app tests

format-check:
	$(PYTHON) -m ruff format --check app tests

test:
	$(PYTHON) -m pytest -q

test-docker:
	docker build --target test -t $(TEST_IMAGE) .

check: lint format-check test

check-docker: test-docker

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs --tail=100 api

status:
	docker compose ps

build:
	docker build --target runtime -t $(IMAGE) .

incident:
	docker compose --profile incident-db-url up --build -d
