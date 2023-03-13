VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
pip=$(VENV)/bin/pip3
django=$(python) manage.py

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'

HOST:=127.0.0.1
PORT:=8001


.PHONY: clean
clean:
	@echo -e $(bold)Clean up old virtualenv and cache$(sgr0)
	rm -rf $(VENV) *.egg-info .pytest_cache

.PHONY: venv
venv: clean
	@echo -e $(bold)Create virtualenv$(sgr0)
	python3.10 -m venv $(VENV)
	$(pip) install --upgrade pip pip-tools

.PHONY: freeze
freeze:
	$(python) -m piptools compile --upgrade --resolver backtracking \
		--extra prod -o requirements.txt pyproject.toml
	$(python) -m piptools compile --upgrade --resolver backtracking \
		--extra prod --extra dev --extra test \
		-o requirements.dev.txt pyproject.toml


# Development Environment
.PHONY: bootstrap develop scss

bootstrap: venv develop

develop:
	@echo -e $(bold)Install and update requirements$(sgr0)
	$(python) -m pip install -r requirements.dev.txt
	$(python) -m spacy download it_core_news_sm
	$(python) -m pip install --editable .

scss:
	$(python) scripts/compile_scss.py

.PHONY: serve
serve: scss
	$(VENV)/bin/uvicorn voices.asgi:app --reload --host $(HOST) --port $(PORT)


.PHONY: test
test:
	$(python) -m pytest 


# Production Environment
.PHONY: production

production: clean
	@echo -e $(bold)Install and update requirements$(sgr0)
	python3.10 -m venv $(VENV)
	$(python) -m pip install -r requirements.txt
	$(python) -m spacy download it_core_news_sm
	$(python) -m pip install --editable .


# Database Management
.PHONY: backup restore

backup:
	pg_dump voci > voci."$(date --iso-8601=seconds)".backup 

restore:
	psql voci < $(shell ls db/voci.* | head -1)
	

# Django commands
.PHONY: run migrate bootstrap-django

bootstrap-django: migrate
	@echo -e $(bold)Initialize django development environment$(sgr0)
	rm -rf db.sqlite3 .media .static
	$(django) migrate
	$(django) createsuperuser --username=admin --email=voci@afor.dev

run:
	$(django) runserver $(HOST):$(PORT)
	
migrate:
	$(django) migrate