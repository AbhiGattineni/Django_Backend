FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /DJANGO_BACKEND

COPY requirements.txt requirements.txt

# ✅ Force pip upgrade and install numpy separately first
RUN pip install --upgrade pip && \
    pip install numpy==1.23.5 && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
