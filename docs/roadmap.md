# Roadmap

- [ ] Move test to django
- [ ] Add support to PostgreSQL and PostGIS
- [ ] Privacy and cookies page
- [ ] Improve how axios show messages in SharePage

- [ ] Test STT for errors
- [ ] Enable italian language recognition in PocketSphinx. Follow this [link](https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst#installing-other-languages)


## Future improvements
- [ ] Add Landscapes models to manage different maps and places
- [ ] Create model abstract classes to manage slug, created/updated fields, ...


## v0.2.0 | Django
- [x] Enable jazzmin
- [x] Create superuser command
- [x] Delete old scripts folder
- [x] Create Models
  - [x] Share
  - [x] Frequency
  - [x] Place
- [x] Install SpatiaLite and GeoDjango 
  [tutorial](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/tutorial/), [installation](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/)
- [x] Delete old templates folder
- [x] Delete old www static folder
- [x] Uninstall sqladmin
- [x] remove starlette commands
- [x] Uninstall SQLModel and fastapi
- [x] Remove api, db amd settings module
- [x] use name resolution for links
- [x] Uninstall pydantic
- [x] Remove repos, handlers, cases (merged in apps)
- [x] Move SpeechToText to django
- [x] Remove old app
- [x] Add signal to save frequencies on Share save
- [x] Complete share template
- [x] Unistall starlette, Pydantic, ...
- [x] Automate Spacy model download
- [x] Update how spacy handle tokens
- [x] Add basic file logging and support for loguru in Django