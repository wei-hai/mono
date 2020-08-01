#!/bin/sh

cd /app
PYTHONPATH=$PWD alembic upgrade head
python -m application.driver --host 0.0.0.0 --port 8080
