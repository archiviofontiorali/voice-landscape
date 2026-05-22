# Voice Landscape − Paesaggio di Voci

## Requirements
- A `python>=3.12` environment
- `uv` available in `PATH`
- Package `ffmpeg` available on the system (for transcription feature)
- A [spatialite](https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/spatialite/) or [postgis](https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/postgis/) ready database 

### Spatialite
You need to install dependencies, set a valid spatialite path in `.env` (default: spatialite:///db.sqlite3) and launch last command if needed

```sh
# On Ubuntu
$ sudo apt install gdal-bin libsqlite3-mod-spatialite
# On Archlinux
$ sudo pacman -S gdal libspatialite

$ uv run python app/manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";
```

## Installation (dev)
```sh
# Create virtualenv, install dependencies
$ uv sync  

# Create superuser
$ uv run app/manage.py createsuperuser --username=admin
# Create new migrations
$ uv run app/manage.py makemigrations
```


## Note for developer
As this project uses a non standard Django Structure some additional care are needed
- manage.py, apps and main app are all inside the app/ folder
- before creating a new app with manage.py is required to enter the app folder otherwise `startapp` command will error out over a module name conflict

## TODO:
- [ ] Ensure that when GPS location is retrieved, place is deselected
- [ ] Implement get_nearest for GeoDjango mode disabled
