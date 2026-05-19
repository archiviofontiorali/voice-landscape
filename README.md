# Voice Landscape − Paesaggio di Voci

## Requirements
- A `python>=3.12` environment
- `uv` available in `PATH`
- 

## Installation (dev)
```sh
# Create virtualenv, install dependencies
$ uv sync  
```


## Note for developer
As this project uses a non standard Django Structure some additional care are needed
- manage.py, apps and main app are all inside the app/ folder
- before creating a new app with manage.py is required to enter the app folder otherwise `startapp` command will error out over a module name conflict
