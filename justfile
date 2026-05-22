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
    uv sync --update

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

# --- Database Management --- #
[confirm('Apply migrations? [y/N]')]
migrate:
    uv run {{ django }} migrate

[confirm('This will DELETE your sqlite database, are you sure? [y/N]')]
db-reset:
    rm -f db.sqlite3
    uv run {{ django }} migrate
    uv run {{ django }} loaddata website

# --- Notebook (marimo) --- #
marimo:
    uv sync --group lab
    uv run marimo edit
