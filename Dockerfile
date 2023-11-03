FROM python:3.10-buster

RUN mkdir /app
WORKDIR /app

COPY req.txt .
RUN pip install -r req.txt

RUN mkdir /app/src
COPY main.py .
COPY alembic.ini .
COPY src/ ./src
