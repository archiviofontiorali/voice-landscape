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

# serve:
# migrate:
# makemigrations:

# shell:
# marimo:

# db stuff
