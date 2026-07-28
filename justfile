# --- Project management --- #
init: clean install
    @echo "Create virtualenv"
    uv sync

[confirm('Do you want to remove existing venv? [y/N]')]
clean:
    find . -regex '^.*\(__pycache__\|\.py[co]\)$' -delete
    rm -rf .venv *.egg-info .pytest_cache

install:
    @echo "Install dependencies"
    uv sync
    # npm install

alias upgrade := update
update:
    @echo "Update dependencies"
    uv sync --upgrade
    uv pip compile pyproject.toml -o requirements.txt
    uv pip compile pyproject.toml --group dev -o requirements.dev.txt
    uv pip compile pyproject.toml --group lab -o requirements.lab.txt

# --- Development commands --- #
host := env("HOST", 'localhost')
port := env("PORT", '8000')
django := "app/manage.py"

show:
    uv run {{ django }} runscript show_settings

[default]
serve: show
    @echo "Launch Django development server"
    uv run {{ django }} runserver {{ host }}:{{ port }}

# --- Production utilities --- #
django-collect:
    uv run {{ django }} collectstatic --ignore=*.scss
    uv run {{ django }} compilescss --use-storage

# --- Database Management --- #
db-init: db-clean db-spatialite-fix db-migrate db-superuser

[confirm('This will DELETE your sqlite database, are you sure? [y/N]')]
db-clean:
    rm -f db.sqlite3

db-spatialite-fix:
    uv run {{ django }} shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";  # Needed for compatibility with spatialite 3.36 to 5.0

[confirm('Apply migrations? [y/N]')]
db-migrate:
    uv run {{ django }} migrate

db-superuser:
    uv run {{ django }} createsuperuser

db-demo:
    uv run {{ django }} loaddata fixtures/demo_musei.json

[confirm]
db-backup:
    mkdir -p .backup
    sqlite3 db.sqlite3 ".backup .backup/$(date -u +'%FT%TZ').db"

# --- Notebook (marimo) --- #
marimo:
    uv sync --group lab
    uv run marimo edit
