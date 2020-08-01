PROJECT_NAME:=backend-mono
VIRTUAL_ENV:=venv

# Development
init-venv:
	python -m venv $(VIRTUAL_ENV)

install-requirements:
	$(VIRTUAL_ENV)/bin/pip install -r requirements.txt

install-requirements-tests:
	$(VIRTUAL_ENV)/bin/pip install -r requirements-tests.txt

install-all:
	make install-requirements install-requirements-tests

start-infra:
	docker-compose up -d

stop-infra:
	docker-compose down

dev:
	$(VIRTUAL_ENV)/bin/python -m application.driver --host 127.0.0.1 --port 8080 --debug

run:
	$(VIRTUAL_ENV)/bin/python -m application.driver --host 0.0.0.0 --port 8080

test:
	@$(VIRTUAL_ENV)/bin/pytest -c pytest.ini

report: SHELL:=/bin/bash
report:
	$(VIRTUAL_ENV)/bin/codecov

bandit:
	$(VIRTUAL_ENV)/bin/bandit -ll -r application tests

pylint:
	$(VIRTUAL_ENV)/bin/pylint application tests

flake8:
	$(VIRTUAL_ENV)/bin/flake8 application tests

mypy:
	$(VIRTUAL_ENV)/bin/mypy

black:
	$(VIRTUAL_ENV)/bin/black -S --check application tests

check:
	make bandit pylint flake8 mypy black

format:
	$(VIRTUAL_ENV)/bin/black -S application tests

# Database
db-revision:
	PYTHONPATH=$(CURDIR) $(VIRTUAL_ENV)/bin/alembic revision --autogenerate --rev-id $(r) -m $(m)

db-upgrade:
	PYTHONPATH=$(CURDIR) $(VIRTUAL_ENV)/bin/alembic upgrade head

db-downgrade:
	PYTHONPATH=$(CURDIR) $(VIRTUAL_ENV)/bin/alembic downgrade head

# Docker
docker-build:
	docker build -t $(PROJECT_NAME):latest .
