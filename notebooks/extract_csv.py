import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import csv
    import polars as pl

    return mo, pl


@app.cell
def _():
    import os, sys
    import django
    from pathlib import Path

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voices.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    django_project_path = Path().cwd() / "app"
    if str(django_project_path) not in sys.path:
        sys.path.insert(0, str(django_project_path))

    django.setup()
    return (Path,)


@app.cell
def _(pl):
    from website.models import Share, Place

    fields = ["id", "timestamp", "place__slug", "place__title", "message"]

    shares = list(Share.objects.values(*fields))
    shares = pl.DataFrame(shares).rename(
        {"place__title": "place_title", "place__slug": "place_slug"}
    )
    shares
    return (shares,)


@app.cell
def _(Path, mo):
    save_path = Path(".data/shares.tsv")
    save = mo.ui.run_button("success", label="Save TSV")
    mo.hstack([save, mo.md(f"Save in `{save_path}`")])
    return save, save_path


@app.cell
def _(mo, save, save_path, shares):
    mo.stop(not save.value)

    shares.write_csv(save_path, separator="\t")
    mo.md(f"Saved in {save_path}")
    return


if __name__ == "__main__":
    app.run()
