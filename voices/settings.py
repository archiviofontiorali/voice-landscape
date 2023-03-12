import pathlib

from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config(
    "DATABASE_URL",
    cast=str,
    default=f"sqlite://",
)

TEMPLATES = config("TEMPLATES", default="templates")

STATIC_PATH = pathlib.Path("www/")
