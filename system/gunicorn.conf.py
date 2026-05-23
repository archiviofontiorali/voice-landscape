"""
ExecStart=/home/USER/git/voice-landscape/.venv/bin/gunicorn \
            --env DJANGO_SETTINGS_MODULE=voices.settings \
            --chdir app \
            --workers=4 \
            --bind 127.0.0.1:8000 \
            --access-logfile "/home/USER/git/voice-landscape/.log/gunicorn.access.log" \
            --error-logfile "/home/USER/git/voice-landscape/.log/gunicorn.error.log" \
            --log-level info \
            voices.wsgi
"""

import multiprocessing
import os
from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parent.parent

# user = os.getenv("USER", "root")
# group = "www-data"
# pythonpath = str(PROJECT_PATH / "app")

bind = "127.0.0.1:8001"
chdir = "./app"
workers = multiprocessing.cpu_count() + 1
wsgi_app = "voices.wsgi:application"
# raw_env = ["DJANGO_SETTINGS_MODULE=voices.settings"]

loglevel = "info"
accesslog = str(PROJECT_PATH / ".log" / "gunicorn.access.log")
errorlog = str(PROJECT_PATH / ".log" / "gunicorn.error.log")
