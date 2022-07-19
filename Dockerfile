# syntax=docker/dockerfile:1
FROM python:3.10.5-slim
WORKDIR /app
MAINTAINER "Jordan Dawson"
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "WoWzer.py", "run", "--host=0.0.0.0"]
