VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
pip=$(VENV)/bin/python -m pip
django=$(python) manage.py

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'

HOST?=localhost
PORT?=8000


.PHONY: bootstrap clean venv requirements develop develop-lab production

bootstrap: venv develop
bootstrap-prod: venv production

clean:
	@echo -e $(bold)Clean up old virtualenv and cache$(sgr0)
	@rm -rf $(VENV) *.egg-info .pytest_cache

venv: clean
	@echo -e $(bold)Create virtualenv$(sgr0)
	@python3 -m venv $(VENV)
	@$(pip) install --upgrade pip pip-tools

requirements:
	@echo -e $(bold)Create requirements with pip-tools$(sgr0)
	@$(VENV)/bin/pip-compile -vU --resolver backtracking -o requirements.txt pyproject.toml
	@$(VENV)/bin/pip-compile -vU --resolver backtracking --extra dev -o requirements.dev.txt pyproject.toml
	@$(VENV)/bin/pip-compile -vU --resolver backtracking --extra lab -o requirements.lab.txt pyproject.toml
	
develop:
	@echo -e $(bold)Install and update development requirements$(sgr0)
	@$(pip) install -r requirements.dev.txt

develop-lab:
	@echo -e $(bold)Install and update jupyter requirements$(sgr0)
	@$(pip) install -r requirements.lab.txt

production:
	@echo -e $(bold)Install and update production requirements$(sgr0)
	@$(pip) install -r requirements.txt


# Django development commands
.PHONY: lab serve test shell 

serve:
	@$(django) runscript show_settings
	@$(django) runserver $(HOST):$(PORT)

lab:
	@# see: https://docs.djangoproject.com/en/4.2/topics/async/
	@DJANGO_ALLOW_ASYNC_UNSAFE=1 $(django) shell_plus --lab

test:
	@$(python) -m pytest

shell:
	@$(django) shell



# Django production commands
.PHONY: collectstatic

collectstatic:
	@$(django) collectstatic --ignore=*.scss
	@$(django) compilescss --use-storage



# Django database commands
.PHONY: demo migrate migrations secret_key superuser 

demo:
	@LOGURU_LEVEL=INFO $(django) runscript init_demo

migrate:
	@echo -e $(bold)Apply migration to database$(sgr0)
	@$(django) migrate

migrations:
	@echo -e $(bold)Create migration files$(sgr0)
	@$(django) makemigrations

secret_key:
	@$(python) scripts/generate_secret_key.py

superuser:
	@echo -e $(bold)Creating superuser account 'admin'$(sgr0)
	@$(django) createsuperuser --username=admin --email=voci@afor.dev


# Database related commands
.PHONY: bootstrap-sqlite db-flush db-demo pg-dump sqlite-reset

bootstrap-sqlite: sqlite-reset migrate superuser

db-flush:
	@echo -e $(bold)Deleting all data from database$(sgr0)
	@$(django) flush

db-demo: db-flush superuser
	@echo -e $(bold)Loading demo data$(sgr0)
	@$(django) loaddata website/demo
	@$(django) loaddata website/demo_places_202309
	@LOGURU_LEVEL=INFO $(django) runscript add_demo_shares

PG_USER?=$(USER)
PG_NAME?=landscapes

pg-dump:
	@echo -e $(bold)Save backup inside folder '.backup'$(sgr0)
	@mkdir -p .backup/
	@pg_dump -U $(PG_USER) $(PG_NAME) | gzip -9 > .backup/landscapes."$(shell date --iso-8601=seconds)".sql.gz
	
pg-load:
	@echo -e $(bold)Load latest backup inside folder '.backup'$(sgr0)
	@psql -U $(PG_USER) $(PG_NAME) < $(shell ls .backup/landscapes.* | tail -1)

sqlite-reset:
	@echo -e $(bold)Prepare SQLite db with GeoDjango enabled$(sgr0)
	@rm -rf db.sqlite3 .media .static	
	# Temporary solution for https://code.djangoproject.com/ticket/32935 
	@$(django) shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";
