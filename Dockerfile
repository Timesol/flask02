FROM python:3.6-alpine

RUN adduser -D ahoehne

WORKDIR /home/ahoehne

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN apk add python-dev
RUN apk add py-cffi
RUN apk add libffi
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev postgresql-dev
RUN venv/bin/pip install psycopg2
RUN venv/bin/pip install setuptools
RUN venv/bin/pip install --user cffi
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY flask01.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP flask01.py

RUN chown -R ahoehne:ahoehne ./
USER ahoehne

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
