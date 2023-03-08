# Landscape of Voices | Paesaggio di Voci
A project by [AFOr, Archivio delle Fonti Orali](https://afor.dev)

> 🇮🇹 Per leggere le istruzioni in italiano vai in [README-IT.md](/README-it.md) 🇮🇹 


## Production environment instructions
Require at least `python>=3.10`, `pip` and `venv` to work. 
To simplify installation `make` is suggested

```shell
# Automatic installation
$ make production

# Or if you prefer installing manually
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
(venv)$ pip install --editable .
(venv)$ python -m spacy download it_core_news_sm
```

### Dependencies installation on linux
```shell
# Ubuntu/debian
$ sudo apt update
$ sudo apt install python3 python3-pip python3-venv make

# Archlinux
$ sudo pacman -S python python-pip python-virtualenv make
```

### Make it work
```shell
$ source .venv/bin/activate
(venv)$ gunicorn -k uvicorn.workers.UvicornWorker -w 4 demo.asgi:app
```

To enable `nginx` and `gunicorn`, create a systemd unit file and apply HTTPS via 
certbot, follow this 
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
(venv)$ python -m spacy download it_core_news_sm
```

## Execute server
Execute on url http://localhost:8001 with autoreload enabled
```shell
# Execute with autoreload
(venv)$ make serve

(venv)$ uvicorn demo.asgi:app --reload --port 8001
```