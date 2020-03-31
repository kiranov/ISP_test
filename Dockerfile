FROM ubuntu:18.04
MAINTAINER Dmitry Kiranov 'kiranov.dm@phystech.edu'
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]
