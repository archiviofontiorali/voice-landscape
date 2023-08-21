"""
Django's settings for voice landscape project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from pathlib import Path

import dj_database_url
import spacy.symbols
from decouple import config  # noqa

# Project paths

BASE_DIR: Path = Path(__file__).resolve().parent.parent

LOG_ROOT = BASE_DIR / ".log"
DATA_ROOT = BASE_DIR / ".data"

LOG_ROOT.mkdir(exist_ok=True)
DATA_ROOT.mkdir(exist_ok=True)

# WebApp settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

DOMAIN = config("DOMAIN")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=f"localhost 127.0.0.1 [::1]").split()
if DOMAIN not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(DOMAIN)

CORS_ALLOWED_ORIGINS = [
    f"https://${DOMAIN}",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


if DEBUG is False:
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 300
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition
INSTALLED_APPS = [
    "corsheaders",
    "jazzmin",
    "apps.speech.apps.SpeechConfig",
    "apps.website.apps.WebsiteConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django_extensions",
    "qr_code",
    "rest_framework",
    "sass_processor",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "admin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "admin.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_URL = config("DATABASE_URL", default=f"spatialite:///{BASE_DIR}/db.sqlite3")

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    ),
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = config("LANGUAGE_CODE", "it")

TIME_ZONE = config("TIME_ZONE", "Europe/Rome")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_ROOT: Path = config("STATIC_ROOT", default=BASE_DIR / ".static")
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

# Logging
LOG_ROOT.mkdir(exist_ok=True)
LOGURU_LOG_LEVEL = config("LOGURU_LEVEL", "WARNING" if not DEBUG else "INFO")
DJANGO_LOG_LEVEL = config("DJANGO_LOG_LEVEL", "WARNING" if not DEBUG else "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_ROOT / "voices.log"),
        },
    },
    "root": {"handlers": ["file"], "level": DJANGO_LOG_LEVEL},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        }
    },
}

# Additional Modules

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 1000,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    # "dark_mode_theme": "darkly",  # Not working at the moment
}

NOTEBOOK_ARGUMENTS = ["--notebook-dir", "notebooks"]

SPACY_MODEL_NAME = config("SPACY_MODEL_NAME", default="it_core_news_lg")
SPACY_VALID_TOKENS = (
    spacy.symbols.ADJ,
    spacy.symbols.ADV,
    spacy.symbols.NOUN,
    spacy.symbols.NUM,
    spacy.symbols.PROPN,  # Proper noun
    spacy.symbols.VERB,
)

SPEECH_RECOGNITION_DEBUG = config("SPEECH_RECOGNITION_DEBUG", cast=bool, default=False)

DEFAULT_POINT_LATITUDE = config("DEFAULT_POINT_LATITUDE", 44.6488366, cast=float)
DEFAULT_POINT_LONGITUDE = config("DEFAULT_POINT_LONGITUDE", 10.9200867, cast=float)

BLACKLIST_PATH = config("BLACKLIST_PATH", default=None)
