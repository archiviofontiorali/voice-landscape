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
$ .venv/bin/pip3 install -e .
$ .venv/bin/python3 -m spacy download it_core_news_sm
```

To run server
```shell
$ .venv/bin/uvicorn demo.asgi:app 
```