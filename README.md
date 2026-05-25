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

## Going in production
```sh
# (0) install dependencies
$ uv sync --group prod

# (1) Set environment variables inside .env 
$ echo "DEBUG=False" >> .env
$ echo "STATIC_ROOT=/usr/share/nginx/voice-landscape/static" >> .env
$ echo "MEDIA_ROOT=/usr/share/nginx/voice-landscape/media" >> .env

# (2) Setup database and migrations
# Needed for compatibility with spatialite 3.36 to 5.0
$ uv run app/manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";  
$ uv run app/manage.py migrate
$ uv run app/manage.py createsuperuser --username=admin
$ uv run app/manage.py loaddata fixtures/demo_[...].json
# NOTE: remember to add in MEDIA_ROOT file and images needed by fixtures

# (2) Generate static files
$ sudo .venv/bin/python app/manage.py collectstatic --ignore=*.scss
$ sudo .venv/bin/python app/manage.py compilescss --use-storage

# (3) Set gunicorn systemctl file and enable it
$ sudo cp system/voice-landscape.service /etc/systemd/system/
# NOTE: remember to edit the service file to setup user and folders
$ sudo systemctl enable voice-landscape.service
$ sudo systemctl start voice-landscape.service

# (4) Configure nginx
TBD
```


## Note for developer
As this project uses a non standard Django Structure some additional care are needed
- manage.py, apps and main app are all inside the app/ folder
- before creating a new app with manage.py is required to enter the app folder otherwise `startapp` command will error out over a module name conflict

## TODO:
- [ ] Ensure that when GPS location is retrieved, place is deselected
- [ ] Implement get_nearest for GeoDjango mode disabled
- [ ] Make default field in Map admits one for each landscape instead of one for all
- [ ] Simplify the get_landscape() approach in general
- [ ] Use a more robust way to pass configuration from Map view and map.(html|js)
- [ ] Set default x and y value to 0, 0
- [ ] Evaluate if making x,y the lat and lon value, remove blank/null from them with a default of (0, 0), in GEODJANGO mode sync the values with location, otherwise leave them indipendent
- [ ] Make min_frequency a property adjustable in admin page (an attribute for each place or for the map, or either ones)
- [ ] WC canvas (and a sort of filter on frequency) must scale with zoom (maybe not by factor of 2, but a value lesser like 1.1)
- [ ] Map, Overlay and WordCloud settings must be set in django admin page (maybe with a json fields?) and passed to frontend either via axios o fetch()
- [ ] Make options like minWidth for WC more obvious and settable from admin
- [ ] Floor Menù with overflow-x-auto or change to a selector when in small screens
- [ ] Add Shares.loaded to indicate wheter words were been loaded in WordFrequency
- [ ] (idea) Report Screen (with auth) to show tables and metrics with download button for tables' CSV files and figure's PNG files
- [ ] Gamification: add command/script to add places' names with frequency 2/3 in such a way to not leaving places completely void and to challenge user to make it disappear
- [ ] Report: tables/graphs with places with most contibutions/contributors
- [ ] Report/Showcase: show the connections between words
- [ ] Report/Map/Showcase: use attention and clustering mechanisms to associates words with common meanings, an alternative metric to frequencies can be developed from these concept
- [ ] Gamification: QR-Code on showcase must redirect to the TV stand, a tutorial can be developed for this place or for a custom qr-code in showcase
- [ ] (idea) Make VOICES_ENABLE_... options editable inside Landscape
- [ ] When VOICES_ENABLE_RECORDING is False the entire API for whisper must be disabled
