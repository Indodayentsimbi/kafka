FROM python:3.9.16-slim-buster

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install python3-pip -y
RUN mkdir app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ARG CLIENT_TYPE=producers

COPY ${CLIENT_TYPE} ${CLIENT_TYPE}

RUN cd ${CLIENT_TYPE}

CMD ["python3","main.py"]

