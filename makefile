PYTHON_VERSION=3
PACKAGE=demo

VENV=.venv
SHELL=/bin/bash
PIP=$(VENV)/bin/pip3

# Utility scripts to prettify echo outputs
bold := \033[1m
clr := \033[0m


.PHONY: bootstrap
bootstrap: venv develop


.PHONY: clean
clean:
	@echo -e '$(bold)Clean up old virtualenv and cache$(clr)'
	rm -rf $(VENV) $(PACKAGE).egg-info .pytest_cache

.PHONY: venv
venv: clean
	@echo -e '$(bold)Create virtualenv$(clr)'
	virtualenv -p /usr/bin/python$(PYTHON_VERSION) $(VENV)
	$(PIP) install --upgrade pip setuptools

.PHONY: develop
develop:
	@echo -e '$(bold)Install and update requirements$(clr)'
	$(PIP) install --upgrade .[develop]
	$(PIP) install --upgrade .[testing]
	$(PIP) install -e .
	$(VENV)/bin/python -m spacy download it_core_news_sm

.PHONY: serve
serve:
	$(VENV)/bin/uvicorn $(PACKAGE).asgi:app --reload --host 0.0.0.0



.PHONY: test
test:
	$(VENV)/bin/pytest 