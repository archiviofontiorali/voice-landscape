VENV=.venv
SHELL=/bin/bash

python=$(VENV)/bin/python3
pip=$(VENV)/bin/python -m pip
django=$(python) manage.py

# Utility scripts to prettify echo outputs
bold := '\033[1m'
sgr0 := '\033[0m'

HOST:=127.0.0.1
PORT:=8001


.PHONY: bootstrap clean venv requirements develop production

bootstrap: venv develop

clean:
	@echo -e $(bold)Clean up old virtualenv and cache$(sgr0)
	@rm -rf $(VENV) *.egg-info .pytest_cache

venv: clean
	@echo -e $(bold)Create virtualenv$(sgr0)
	@python3.10 -m venv $(VENV)
	@$(pip) install --upgrade pip

requirements:
	@echo -e $(bold)Create requirements with pip-tools$(sgr0)
	@$(python) -m piptools compile -vU --resolver backtracking --all-extras -o requirements.txt pyproject.toml
	
develop:
	@echo -e $(bold)Install and update requirements$(sgr0)
	@$(pip) install -r requirements.txt
	@$(pip) install --editable .

production: clean venv
	@echo -e $(bold)Install and update requirements$(sgr0)
	@$(pip) install .


# Notebooks commands
.PHONY: bootstrap-lab lab
bootstrap-lab:
	@$(pip) install -e .[lab]

lab:
	# see: https://docs.djangoproject.com/en/4.2/topics/async/
	@DJANGO_ALLOW_ASYNC_UNSAFE=1 $(django) shell_plus --lab


# Django development commands
.PHONY: clean-django serve test shell 

clean-django:
	@rm -rf db.sqlite3 .media .static

serve:
	@$(django) runserver $(HOST):$(PORT)

test:
	@$(python) -m pytest 

shell:
	@$(django) shell

secret_key:
	@$(python) scripts/generate_secret_key.py



# Django production commands
.PHONY: collectstatic

collectstatic:
	@$(django) collectstatic --ignore=*.scss
	@$(django) compilescss --use-storage



# Django database commands
.PHONY: bootstrap-django demo migrate migrations superuser sqlite-bootstrap 

bootstrap-django: clean-django secret_key sqlite-bootstrap migrate superuser 

demo:
	@$(django) runscript init_demo

migrate:
	@echo -e $(bold)Apply migration to database$(sgr0)
	@$(django) migrate

migrations:
	@echo -e $(bold)Create migration files$(sgr0)
	@$(django) makemigrations

superuser:
	@$(django) createsuperuser --username=admin --email=voci@afor.dev

sqlite-bootstrap: 
	@echo -e $(bold)Prepare SQLite db with GeoDjango enabled$(sgr0)
	# Temporary solution for https://code.djangoproject.com/ticket/32935 
	@$(django) shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";