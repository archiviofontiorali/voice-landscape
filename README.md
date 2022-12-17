# afor-paesaggio-di-voci

## Development installation
Require `python>=3.8`, `pip`, and `make` installed on your machine
```shell
$ make bootstrap
```

For launching with reload enabled
```shell
$ make serve
```


## Local installation
Require `python>=3.8`, `pip` and `venv` installed
```shell
# ubuntu
$ sudo apt install python3 python3-pip python3-venv
```

Clone repository and enter folder

```shell
$ python3 -m venv .venv
$ .venv/bin/pip3 install --upgrade pip setuptools
$ .venv/bin/pip3 install --upgrade gunicorn
$ .venv/bin/pip3 install -e .
$ .venv/bin/python3 -m spacy download it_core_news_sm
```

To run server
```shell
# Development 
$ .venv/bin/uvicorn demo.asgi:app --reload
# Production 
$ .venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 4 demo.asgi:app
```

To enable `nginx` and `gunicorn`, create a systemd unit file and apply HTTPS via 
certbot, follow this 
[tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
(ubuntu 20.04) 


Example:
```ini
[Unit]
Description=Gunicorn instance to run Paesaggio di Voci
After=network.target

[Service]
User=<YOUR USER>
Group=www-data
WorkingDirectory=/home/<YOUR USER>/git/afor-paesaggi-di-voci
Environment="PATH=/usr/bin:/home/<YOUR USER>/git/afor-paesaggi-di-voci/.venv/bin"
ExecStart=/home/<YOUR USER>/git/afor-paesaggi-di-voci/.venv/bin/gunicorn -w 4 --bind unix:voci.afor.dev.sock -k uvicorn.workers.UvicornWorker -m 007 demo.asgi:app

[Install]
WantedBy=multi-user.target
```