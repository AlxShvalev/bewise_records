FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN apt-get -y update

RUN apt-get -y upgrade

RUN apt-get -y install ffmpeg

CMD uvicorn main:app --host 0.0.0.0 --port 8080 --reload
