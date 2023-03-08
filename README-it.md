# Paesaggio di Voci (Voice Landscape)
Un progetto sviluppato da [AFOr, Archivio delle Fonti Orali](https://afor.dev)

> For International English language instructions go to [README.md](/README.md) 


## Instruzioni installazione (produzione)
Richiede `python>=3.10`, `pip` e `venv`. 
`make` è consigliato per semplificare l'installazione

```shell
# Installazione guidata
$ make production

# Installazione manuale
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
(venv)$ pip install --editable .
(venv)$ python -m spacy download it_core_news_sm
```

### Installazione dipendenze su linux
```shell
# Ubuntu/debian
$ sudo apt update
$ sudo apt install python3 python3-pip python3-venv make

# Archlinux
$ sudo pacman -S python python-pip python-virtualenv make
```

### Come usarlo
```shell
$ source .venv/bin/activate
(venv)$ gunicorn -k uvicorn.workers.UvicornWorker -w 4 demo.asgi:app
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
Richiede `python>=3.10`, `pip` e `venv`. 
`make` è consigliato per semplificare l'installazione

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