FROM ubuntu:22.04

MAINTAINER Kirill Cymbaliuk <kirill.lego-kot@ya.ru>

RUN apt-get update
RUN apt-get install -y git

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip

RUN git clone https://github.com/Kirill72-web/DataHack.git
WORKDIR DataHack

RUN pip3 install -r requirements.txt
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install spark
RUN pip3 install