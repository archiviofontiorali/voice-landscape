FROM python:3.11

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0
ENV DATABASE_URL=postgis://postgres:lv-password@db:5432/landscapes
ENV SPACY_MODEL_NAME=it_core_news_lg


RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install gdal-bin ffmpeg

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

RUN python -m spacy download $SPACY_MODEL_NAME

COPY manage.py /app/
COPY admin/ /app/admin/
COPY apps/ /app/apps/
COPY scripts/ /app/scripts/

RUN python scripts/generate_secret_key.py
CMD python manage.py runserver 0.0.0.0:8000