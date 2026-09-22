.PHONY: up down logs status test build incident

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs --tail=100 api

status:
	docker compose ps

test:
	python -m compileall app

build:
	docker build -t order-api:local .

incident:
	docker compose --profile incident-db-url up --build -d
