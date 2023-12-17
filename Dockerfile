FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /DJANGO_BACKEND

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .