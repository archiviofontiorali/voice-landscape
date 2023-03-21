# Paesaggio di Voci (Voice Landscape)
Un progetto sviluppato da [AFOr, Archivio delle Fonti Orali](https://afor.dev)

> For International English language instructions go to [README.md](/README.md) 

## Instruzioni installazione (produzione)
Richiede `python>=3.10`, `pip` e `venv`. 
`make` è consigliato per semplificare l'installazione

### Installazione dipendenze su linux
```shell
# Ubuntu/debian
$ sudo apt update
$ sudo apt install python3 python3-pip python3-venv make

# Archlinux
$ sudo pacman -S python python-pip python-virtualenv make
```

## Istruzioni per inizializzazione Database
Questo pacchetto usa [GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/tutorial/) 
per gestire funzionalità geografiche come distanze e coordinate. Alcuni pacchetti aggiuntivi sono richiesti:
- [GDAL](https://gdal.org/) 
- [spatiallite](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/spatialite/) if using sqlite db
- [PostGIS](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/postgis/) if using PostgreSQL
- MySQL non è attualmente supportato


### Preparazione per SQLite
Installa GDAL e Spatialite
```shell
# On ubuntu
$ sudo apt install gdal-bin libsqlite3-mod-spatialite

# On archlinux
$ sudo pacman -S gdal libspatialite
```

Imposta un percorso SQLite valido (di tipo spatialite) in `.env` (default: spatialite:///db.sqlite)

Inizializza Spatialite e applica le migrazioni
```shell
# Automatic
$ make bootstrap-sqlite migrate

# Manually
$ source .venv/bin/activate
(.venv)$ python manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";
(.venv)$ python manage.py migrate
```


### Preparazione per PostgreSQL
Installa GDAL e PostGIS
```shell
# On ubuntu (<x> is the postgres version)
$ sudo apt install gdal-bin postgresql-<x>-postgis-3  

# On archlinux
$ sudo pacman -S gdal postgis
```

Imposta un percorso PostgreSQL valido (di tipo PostGIS) in `.env` (example: postgis://...)
Ricorda che di default questa app usa sqlite

Crea il DB e abilita PostGIS (dipende da come hai installato postgres sul tuo sistema, 
in system/ è presente un docker-compose file per creare un istanza postgres con docker)
```shell
# For more info go to https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/postgis/
$ createdb  <db name>
$ psql <db name>
> CREATE EXTENSION postgis;
```

Applica le migrazioni
```shell
# Automatic
$ make migrate

# Manually
(.venv)$ python manage.py migrate
```

## Ambiente di produzione

### Installazione repository
```shell
# Installazione guidata
$ make production

# Installazione manuale
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
(venv)$ pip install --editable .
```

### Come avviare il server in produzione
```shell
$ source .venv/bin/activate
(venv)$ gunicorn admin.wsgi
```

Per abilitare `nginx` e `gunicorn` all'avvio, crea un `systemd unit file` e usa 
`certbot` per l'HTTPS 
[tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
(ubuntu 20.04) 

Un file service systemd lo potete trovare in 
[voice-landscape.service](/system/voice-landscape.service)

Il service assume che il progetto sia stato clonato all'interno di una cartella `git` 
all'interno della `home` dell'utente
Ricorda di cambiare `<YOUR USER>` con il nome del tuo utente

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