FROM python:alpine

LABEL AUTHOR="Leandro Alves <alves.engleandro@gmail.com>"
LABEL VERSION="v1.0.0"
LABEL UPDATE_AT="2021.10.23"
LABEL CAPTION="Interface API: External Communication with Clients"

WORKDIR src/user/app

RUN apt upgrade && apt install -y tini
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
