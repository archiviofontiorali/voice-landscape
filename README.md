# Landscape of Voices | Paesaggio di Voci
A project by [AFOr, Archivio delle Fonti Orali](https://afor.dev)

> 🇮🇹 Per leggere le istruzioni in italiano vai in [README-IT.md](/README-it.md) 🇮🇹 

## System dependencies installation
Require at least `python>=3.10`, `pip` and `venv` to work.
To simplify installation `make` is suggested

```shell
# Ubuntu/debian
$ sudo apt update
$ sudo apt install python3 python3-pip python3-venv make

# Archlinux
$ sudo pacman -S python python-pip python-virtualenv make
```

## Database instructions
This Django app uses [GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/tutorial/) 
to handle spatial features like coordinates. Some additional package are required to use database
- [GDAL](https://gdal.org/) 
- [spatiallite](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/spatialite/) if using sqlite db
- [PostGIS](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/postgis/) if using PostgreSQL
- MySQL is not supported or tested at the moment 

### Prepare SQLite
Install GDAL and Spatialite dependencies
```shell
# On ubuntu
$ sudo apt install gdal-bin libsqlite3-mod-spatialite

# On archlinux
$ sudo pacman -S gdal libspatialite
```

Set a valid SQLite path in `.env` file (default: sqlite:///db.sqlite)

Enable Spatialite and migrations by executing 
```shell
# Automatic
$ make bootstrap-sqlite migrate

# Manually
$ source .venv/bin/activate
(.venv)$ python manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";
(.venv)$ python manage.py migrate
```

### Prepare PostgreSQL
Install GDAL and PostGIS dependencies
```shell
# On ubuntu (<x> is the postgres version)
$ sudo apt install gdal-bin postgresql-<x>-postgis-3  

# On archlinux
$ sudo pacman -S gdal postgis
```

Set a valid PostgreSQL path in `.env` file (default: sqlite:///db.sqlite)

Create DB and enable PostGIS (this also depend on which way you installed postgres) 
```shell
# For more info go to https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/postgis/
$ createdb  <db name>
$ psql <db name>
> CREATE EXTENSION postgis;
```

Then make migrations
```shell
# Automatic
$ make migrate

# Manually
(.venv)$ python manage.py migrate
```

## Production environment instructions

### Install repository
```shell
# Automatic installation
$ make production

# Or if you prefer installing manually
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
(venv)$ pip install --editable .
```

### Launch server
```shell
$ source .venv/bin/activate
(venv)$ gunicorn -w 4 admin.wsgi
```

To enable `nginx` and `gunicorn` on boot, create a systemd unit file and apply HTTPS via 
certbot, following this 
[tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
(ubuntu 20.04) 

An example systemd service file is located in [voice-landscape.service](/system/voice-landscape.service)
It assumes you clone this repository inside your user folder inside a `git` folder
Remember to change `<YOUR USER>` with your effective user

```shell
$ cd ~ && mkdir -p git 
$ git clone https://github.com/archiviofontiorali/voice-landscape ~/git/
```


## Development instructions
Require at least `python>=3.10`, `pip` and `venv` to work. 
To simplify installation `make` is suggested

```shell
$ make bootstrap

# Or if you prefer installing manually
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv)$ pip install --upgrade pip pip-tools
(venv)$ pip install -r requirements.dev.txt
(venv)$ pip install --editable .
```

## Execute server
Execute on url http://localhost:8001 with autoreload enabled
```shell
# Execute with autoreload
(venv)$ make serve

(venv)$ python manage.py runserver http://localhost:8001
```