FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y python-dev build-essential python-setuptools python-pip git libcurl4-openssl-dev libssl-dev libffi-dev

RUN mkdir /app
WORKDIR /app

ADD requirements/base requirements/base
RUN pip install -r requirements/base

ADD app app/
ADD payee payee/
ADD manage.py manage.py

CMD gunicorn --workers $GUNICORN_WORKERS \
--access-logfile /dev/stdout \
--error-logfile /dev/stderr \
--bind=0.0.0.0:$PORT \
--timeout=100 \
--graceful-timeout=120 \
payee.wsgi \
