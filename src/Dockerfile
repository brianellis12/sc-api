FROM python:3.11

RUN apt-get update

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8008