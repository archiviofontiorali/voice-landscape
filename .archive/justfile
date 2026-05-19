VENV := ".venv"

python := VENV/"bin/python3"
django := python + " manage.py"
database := 'db.sqlite3'
host := 'localhost'
port := '8000'

alias upgrade := update

[confirm('Do you want to remove existing venv? [y/N]')]
venv:
    @echo "Create virtualenv"
    rm -rf .venv *.egg-info .pytest_cache
    uv venv --python ">=3.13" {{VENV}}
    npm install

freeze:
    uv pip compile -U pyproject.toml -o requirements.txt

install:
    uv pip install -r requirements.txt
    uv pip install --editable .

install-dev:
    uv pip install -r requirements.txt
    uv pip install --editable .[dev]

update: freeze install

[default]
serve:
    @echo "Launch Django development server"
    {{ django }} runscript show_settings
    {{ django }} runserver {{host}}:{{port}}

test:
	@{{ python }} -m pytest


django-shell:
    @{{ django }} shell

[confirm('Apply migrations? [y/N]')]
django-migrate:
    @{{ django }} migrate

django-collect:
    {{ django }} collectstatic --ignore=*.scss
    {{ django }} compilescss --use-storage

[confirm]
backup:
    mkdir -p .backup
    sqlite3 {{ database }} ".backup .backup/$(date -u +'%FT%TZ').db"

[confirm('This will delete all data inside db.sqlite3. Are you sure? [y/N]')]
reset-sqlite:
	@echo Prepare SQLite db with GeoDjango enabled
	@rm -rf db.sqlite3 .media .static
	# Temporary solution for https://code.djangoproject.com/ticket/32935
	@{{ django }} shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";

superuser:
	@echo Creating superuser account 'admin'
	@{{ django }} createsuperuser --username=admin --email=voci@afor.dev

demo: reset-sqlite django-migrate superuser
	@echo Loading demo data
	@{{ django }} loaddata website/demo
	@{{ django }} loaddata website/demo_places_202309
	@LOGURU_LEVEL=INFO {{ django }} runscript add_demo_shares
