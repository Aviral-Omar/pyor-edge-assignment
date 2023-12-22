# syntax=docker/dockerfile:1

FROM python:3.9.18-slim-bullseye

WORKDIR /pyor-api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "--app", "flask_app", "run", "--host=0.0.0.0"]
