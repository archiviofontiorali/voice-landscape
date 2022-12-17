VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
pip=$(VENV)/bin/pip3

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'

HOST:=127.0.0.1
PORT:=8001

.PHONY: bootstrap
bootstrap: venv develop


.PHONY: clean
clean:
	@echo -e $(bold)Clean up old virtualenv and cache$(sgr0)
	rm -rf $(VENV) .pytest_cache

.PHONY: venv
venv: clean
	@echo -e $(bold)Create virtualenv$(sgr0)
	python3.10 -m venv $(VENV)
	$(pip) install --upgrade pip pip-tools

.PHONY: freeze
freeze:
	$(VENV)/bin/pip-compile

.PHONY: production
production:
	@echo -e $(bold)Install and update requirements$(sgr0)
	$(pip) install -r requirements.txt
	$(VENV)/bin/python -m spacy download it_core_news_sm

.PHONY: develop
develop: production
	$(pip) install --upgrade isort black pytest

.PHONY: scss
scss:
	$(python) scripts/compile_scss.py

.PHONY: serve
serve: scss
	$(VENV)/bin/uvicorn demo.asgi:app --reload --host $(HOST) --port $(PORT)

.PHONY: test
test:
	$(VENV)/bin/pytest 
	

.PHONY: backup
backup:
	sqlite3 db/db.sqlite .dump | tar czvf > db/$(shell date +"%Y-%m-%dT%H:%M:%S%z").tar.gz 
	