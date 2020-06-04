PROJECT_NAME:=mono
VIRTUAL_ENV:=env

# Development
init-env:
	python -m venv $(VIRTUAL_ENV)

install-requirements:
	$(VIRTUAL_ENV)/bin/pip install -r requirements.txt

install-requirements-tests:
	$(VIRTUAL_ENV)/bin/pip install -r requirements-tests.txt

install-all:
	make install-requirements install-requirements-tests

start-test-env:
	docker-compose up -d

stop-test-env:
	docker-compose down

debug:
	$(VIRTUAL_ENV)/bin/python -m application.driver --host 127.0.0.1 --port 8080 --debug --auto_reload --worker 1

run:
	$(VIRTUAL_ENV)/bin/python -m application.driver --host 0.0.0.0 --port 8080

test:
	$(VIRTUAL_ENV)/bin/pytest

pylint:
	$(VIRTUAL_ENV)/bin/pylint application

flake8:
	$(VIRTUAL_ENV)/bin/flake8 application

mypy:
	$(VIRTUAL_ENV)/bin/mypy

check:
	make pylint flake8 mypy

# Database
db-revision:
	PYTHONPATH=$(CURDIR) $(VIRTUAL_ENV)/bin/alembic revision --autogenerate --rev-id $(r) -m $(m)

db-upgrade:
	PYTHONPATH=$(CURDIR) $(VIRTUAL_ENV)/bin/alembic upgrade head

db-downgrade:
	PYTHONPATH=$(CURDIR) $(VIRTUAL_ENV)/bin/alembic downgrade head

# Docker
docker-build:
	docker build -t mono:latest .
