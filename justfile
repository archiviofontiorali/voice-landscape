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
host := 'localhost'
port := '8000'

[default]
serve:
    @echo "Launch Django development server"
    uv run manage.py runserver {{ host }}:{{ port }}

# migrate:
# makemigrations:

# shell:
# marimo:

# db stuff
