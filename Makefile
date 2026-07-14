.PHONY: install lint test docker-check run-api ingest reindex chat-demo eval

install:
	pip install -e .[dev]

lint:
	ruff check src tests

test:
	pytest

docker-check:
	docker compose config

run-api:
	uvicorn knowledge_agent.api.app:app --reload

ingest:
	knowledge-agent ingest --recreate

reindex:
	knowledge-agent reindex

chat-demo:
	knowledge-agent chat-demo --question "$${QUESTION:-How should API keys be stored?}"

eval:
	knowledge-agent eval --output-path reports/eval_report.json
