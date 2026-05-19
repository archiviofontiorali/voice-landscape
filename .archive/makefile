VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
pip=$(VENV)/bin/python -m pip
django=$(python) manage.py

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'


# Django production commands
# .PHONY: collectstatic

# collectstatic:
# 	@$(django) collectstatic --ignore=*.scss
# 	@$(django) compilescss --use-storage



# Django database commands
.PHONY: demo migrate migrations secret_key superuser

secret_key:
	@$(python) scripts/generate_secret_key.py


demo: db-flush
	@echo -e $(bold)Loading demo data$(sgr0)
	@$(django) loaddata website/demo
	@$(django) loaddata website/demo_places_202309
	@LOGURU_LEVEL=INFO $(django) runscript add_demo_shares


# Database related commands
.PHONY: db-flush pg-dump

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
