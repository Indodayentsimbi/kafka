FROM python:3.9.16-slim-buster

ARG CLIENT_TYPE=producers

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y
RUN mkdir app

WORKDIR /app/${CLIENT_TYPE}

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ${CLIENT_TYPE} .

CMD ["python3","main.py"]