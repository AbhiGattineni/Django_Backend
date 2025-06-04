FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /DJANGO_BACKEND

COPY requirements.txt requirements.txt

RUN pip install numpy==1.23.5 && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "makemigrations"]