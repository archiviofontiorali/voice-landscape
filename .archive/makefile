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

# Django development commands
# .PHONY: lab serve test shell

# serve:
# 	@echo -e $(bold)Launch Django development server$(sgr0)
# 	@$(django) runscript show_settings
# 	@$(django) runserver $(HOST):$(PORT)

lab:
	@# see: https://docs.djangoproject.com/en/4.2/topics/async/
	@DJANGO_ALLOW_ASYNC_UNSAFE=1 $(django) shell_plus --lab

# shell:
# 	@$(django) shell



# Django production commands
# .PHONY: collectstatic

# collectstatic:
# 	@$(django) collectstatic --ignore=*.scss
# 	@$(django) compilescss --use-storage



# Django database commands
.PHONY: demo migrate migrations secret_key superuser

# migrate:
# 	@echo -e $(bold)Apply migration to database$(sgr0)
# 	@$(django) migrate

migrations:
	@echo -e $(bold)Create migration files$(sgr0)
	@$(django) makemigrations

secret_key:
	@$(python) scripts/generate_secret_key.py

superuser:
	@echo -e $(bold)Creating superuser account 'admin'$(sgr0)
	@$(django) createsuperuser --username=admin --email=voci@afor.dev

demo: db-flush superuser
	@echo -e $(bold)Loading demo data$(sgr0)
	@$(django) loaddata website/demo
	@$(django) loaddata website/demo_places_202309
	@LOGURU_LEVEL=INFO $(django) runscript add_demo_shares


# Database related commands
.PHONY: bootstrap-sqlite db-flush pg-dump sqlite-reset

bootstrap-sqlite: sqlite-reset migrate superuser

db-flush:
	@echo -e $(bold)Deleting all data from database$(sgr0)
	@$(django) flush


PG_USER?=$(USER)
PG_NAME?=landscapes

pg-dump:
	@echo -e $(bold)Save backup inside folder '.backup'$(sgr0)
	@mkdir -p .backup/
	@pg_dump -U $(PG_USER) $(PG_NAME) | gzip -9 > .backup/landscapes."$(shell date --iso-8601=seconds)".sql.gz

pg-load:
	@echo -e $(bold)Load latest backup inside folder '.backup'$(sgr0)
	@gzip -dk $(shell ls .backup/landscapes.*.gz | tail -1) || true
	@psql -U $(PG_USER) $(PG_NAME) < $(shell ls .backup/landscapes.*.sql | tail -1)

pg-reset:
	@dropdb -U $(PG_USER) $(PG_NAME)
	@createdb -U $(PG_USER) $(PG_NAME)

sqlite-reset:
	@echo -e $(bold)Prepare SQLite db with GeoDjango enabled$(sgr0)
	@rm -rf db.sqlite3 .media .static
	# Temporary solution for https://code.djangoproject.com/ticket/32935
	@$(django) shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";
