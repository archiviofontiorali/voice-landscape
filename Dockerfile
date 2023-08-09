FROM python:3.11

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install gdal-bin

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY .env /app/
COPY manage.py /app/
COPY admin/ /app/admin/
COPY apps/ /app/apps/

RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000