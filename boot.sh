#!/bin/sh
source venv/bin/activate
flask db upgrade
flask translate compile
exec gunicorn -b 10.146.177.50:5000 --access-logfile - --error-logfile - flask01:app
