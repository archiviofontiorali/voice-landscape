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
DEBUG?=1


.PHONY: bootstrap clean venv requirements develop production

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
	@$(VENV)/bin/pip-compile -vU --resolver backtracking --all-extras -o requirements.dev.txt pyproject.toml
	
develop:
	@echo -e $(bold)Install and update development requirements$(sgr0)
	@$(pip) install -r requirements.dev.txt

production:
	@echo -e $(bold)Install and update production requirements$(sgr0)
	@$(pip) install -r requirements.txt


# Django development commands
.PHONY: lab serve test shell 

serve:
	@DEBUG=$(DEBUG) $(django) runserver $(HOST):$(PORT)

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
.PHONY: bootstrap-django clean-django demo migrate migrations secret_key superuser sqlite-bootstrap 

bootstrap-django: clean-django secret_key sqlite-bootstrap migrate superuser 

clean-django:
	@rm -rf db.sqlite3 .media .static

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
	@$(django) createsuperuser --username=admin --email=voci@afor.dev

sqlite-bootstrap: 
	@echo -e $(bold)Prepare SQLite db with GeoDjango enabled$(sgr0)
	# Temporary solution for https://code.djangoproject.com/ticket/32935 
	@$(django) shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";

