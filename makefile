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
.PHONY: serve bootstrap develop test

bootstrap: venv develop

develop:
	@echo -e $(bold)Install and update requirements$(sgr0)
	$(python) -m pip install -r requirements.dev.txt
	$(python) -m pip install --editable .

serve:
	$(django) runserver $(HOST):$(PORT)

test:
	$(python) -m pytest 



# Production Environment
.PHONY: production

production: clean
	@echo -e $(bold)Install and update requirements$(sgr0)
	python3.10 -m venv $(VENV)
	$(python) -m pip install -r requirements.txt
	$(python) -m pip install .



# Django commands
.PHONY: bootstrap-django clean-django migrate migrations shell superuser

bootstrap-django: clean-django migrate superuser 

clean-django:
	rm -rf db.sqlite3 .media .static

migrate:
	$(django) migrate

migrations:
	$(django) makemigrations

shell:
	$(django) shell

superuser:
	$(django) createsuperuser --username=admin --email=voci@afor.dev

generate_secret_key:
	@$(python) -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"



# Database Management
.PHONY: pg-backup pg-restore sqlite-bootstrap

pg-backup:
	pg_dump voci > voci."$(date --iso-8601=seconds)".backup 

pg-restore:
	psql voci < $(shell ls db/voci.* | head -1)

sqlite-bootstrap: 
	@echo -e $(bold)Prepare SQLite db with GeoDjango enabled$(sgr0)
	# Temporary solution for https://code.djangoproject.com/ticket/32935 
	$(django) shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";


# Demo commands
.PHONY: bootstrap-demo
 
bootstrap-demo:
	$(django) runscript init_demo
	