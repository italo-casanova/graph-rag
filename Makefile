.PHONY: dev up wait models venv db ingest run logs clean

COMPOSE=docker compose
PYTHON=python3
VENV=.venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python

dev: up wait venv models db ingest run

up:
	@echo "Starting containers..."
	$(COMPOSE) up -d

wait:
	@echo "Waiting for Postgres..."
	until docker exec rag-postgres pg_isready -U postgres; do \
		sleep 2; \
	done

	@echo "Waiting for Ollama..."
	until curl -s http://localhost:11434 > /dev/null; do \
		sleep 2; \
	done

	@echo "Waiting for Gremlin..."
	until nc -z localhost 8182; do \
		sleep 2; \
	done

	@echo "All services ready."

venv:
	@echo "Setting up virtual environment..."
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

models:
	@echo "Installing Ollama models..."
	curl http://localhost:11434/api/pull -d '{"name":"nomic-embed-text"}'
	curl http://localhost:11434/api/pull -d '{"name":"llama3"}'

db:
	@echo "Initializing Postgres..."
	docker exec -i rag-postgres psql -U postgres -d rag < sql/init.sql

ingest:
	@echo "Running document ingestion..."
	$(PY) -m ingestion.ingest_documents

run:
	@echo "Starting API..."
	$(PY) app.py

logs:
	$(COMPOSE) logs -f

clean:
	$(COMPOSE) down -v
