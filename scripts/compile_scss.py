import sass  # noqa
import pathlib 

BASE_DIR = pathlib.Path(".")
STATICFILES_DIRS = BASE_DIR / "www"

CSS_PATH = STATICFILES_DIRS / "css"
SCSS_PATH = STATICFILES_DIRS / "scss"

CSS_PATH.mkdir(exist_ok=True)
SCSS_PATH.mkdir(exist_ok=True)

sass.compile(dirname=(str(SCSS_PATH), str(CSS_PATH)), output_style="compressed")
