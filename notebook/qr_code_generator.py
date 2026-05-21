import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import django
    import os, sys
    from pathlib import Path

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voices.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    django_project_path = Path().cwd() / "app"
    if str(django_project_path) not in sys.path:
        sys.path.insert(0, str(django_project_path))

    django.setup()


@app.cell
def _():
    from website.models import Place

    return (Place,)


@app.cell
def _(Place):
    for place in Place.objects.all():
        print(place.slug)
    return


if __name__ == "__main__":
    app.run()
