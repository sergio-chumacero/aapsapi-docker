FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY . /aapsapi/
WORKDIR /aapsapi

RUN pip install --no-cache-dir --requirement requirements.txt
