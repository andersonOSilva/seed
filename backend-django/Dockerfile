FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

# Executa o pip
RUN pip install -r requirements.txt

ADD . /code/

RUN python api/manage.py migrate
