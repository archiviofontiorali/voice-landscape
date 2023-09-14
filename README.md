# Landscape of Voices | Paesaggio di Voci
A project by [AFOr, Archivio delle Fonti Orali](https://afor.dev)


## System dependencies installation (either development and production)
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
This Django app uses [GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/tutorial/) to handle spatial features like coordinates.
You can chose between using sqlite3 (with spatialite) and postgres (with postgis). 
For postgis a docker-compose file is available in `system/` folder 
Note that MySQL/mariadb is not supported or tested at the moment 

Some additional package are required to use database:
- [GDAL](https://gdal.org/) 
- [spatiallite](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/spatialite/) if using sqlite db
- [PostGIS](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/postgis/) if using PostgreSQL

Install GDAL and then go to the choosen DB section
```shell
# On ubuntu
$ sudo apt install gdal-bin

# On archlinux
$ sudo pacman -S gdal
```

### Prepare SQLite (manually)
Install GDAL and Spatialite dependencies
```shell
# On ubuntu
$ sudo apt install libsqlite3-mod-spatialite

# On archlinux
$ sudo pacman -S libspatialite
```

Set a valid SQLite path (of type spatialite) in `.env` file 
(default: spatialite:///db.sqlite3)

Enable Spatialite and apply migrations by executing 
```shell
# via makefile
$ make bootstrap-sqlite

# Manually
$ source .venv/bin/activate
(.venv)$ python app/manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";
```

### Prepare PostgreSQL manually
Install PostGIS dependencies
```shell
# On ubuntu (<x> is the postgres version, libpq-dev is required to have a valid licence)
$ sudo apt install libpq-dev postgresql-<x>-postgis-3  
# NOTE: With postgresql-11 and postgis 2.5
$ sudo apt install postgresql-11-postgis-2.5 postgresql-11-postgis-2.5-scripts

# On archlinux
$ sudo pacman -S postgis
```

Set a valid PostgreSQL path (of type PostGIS) in `.env` file (example: postgis://...)

**Remember**: if variable `DATABASE_URL` is not set, by default a sqlite file is used

Create DB and enable PostGIS
```shell
# For more info go to https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/postgis/
$ createdb  <db name>
$ psql <db name>
> CREATE EXTENSION postgis;
```

Some additional step may be needed if you want a custom user or some specific configuration

Apply migrations
```shell
# via makefile
$ make migrate

# manually (inside environment)
(.venv)$ python app/manage.py migrate
```

### Prepare PostgreSQL with docker-compose
Inside `system/` subfolder you can find a docker-compose.yml to automatically install a 
postgis database with adminer

```shell
$ docker compose -f system/docker-compose.yml up
```

db is available at `postgis://postgres:lv-password@localhost:54320/landscapes` so 
remember to add `DATABASE_URL=postgis://postgres:lv-password@localhost:54320/landscapes` 
inside .env file 

db is linked to a docker volume to preserve data. To reset data you can use: 
```shell
$ python manage.py flush --no-input
```



## Production environment instructions

### Install repository
```shell
# Automatic installation
$ make venv production

# Or if you prefer installing manually
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
```

Apply migrations and create admin user
```shell
# Automatic
$ make secret_key migrate superuser

# Manually
(.venv)$ python scripts/generate_secret_key.py
(.venv)$ python manage.py migrate
(.venv)$ python manage.py createsuperuser
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
$ sudo sh -c "sed 's/USER/$USER/' system/voice-landscape.service > /usr/lib/systemd/system/voice-landscape.service"
$ sudo cp system/nginx.conf /etc/nginx/sites-available/nginx.conf
```

```shell
$ cd ~ && mkdir -p git 
$ git clone https://github.com/archiviofontiorali/voice-landscape ~/git/
```


## Development instructions

```shell
$ make bootstrap

# Or if you prefer installing manually
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
(venv)$ pip install --editable .
```

Apply migrations and create admin user
```shell
# Automatic
$ make migrate createsuperuser

# Manually
(.venv)$ python manage.py migrate
(.venv)$ python manage.py createsuperuser
```

## Execute server
Execute on url http://localhost:8000 with autoreload enabled
```shell
# Execute with autoreload
(venv)$ make serve

(venv)$ python manage.py runserver http://localhost:8000
```