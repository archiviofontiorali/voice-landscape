# Voice Landscape − Paesaggio di Voci

## Requirements
- A `python>=3.12` environment
- `uv` available in `PATH`
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
```


## Note for developer
As this project uses a non standard Django Structure some additional care are needed
- manage.py, apps and main app are all inside the app/ folder
- before creating a new app with manage.py is required to enter the app folder otherwise `startapp` command will error out over a module name conflict
