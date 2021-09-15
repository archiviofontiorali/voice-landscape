import os.path

import databases
from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config(
    "DATABASE_URL",
    cast=databases.DatabaseURL,
    default=f"sqlite:///{os.path.abspath('db/db.sqlite')}",
)
