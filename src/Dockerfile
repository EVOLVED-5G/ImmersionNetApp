# syntax=docker/dockerfile:1
FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

ADD . /usr/src/app/

EXPOSE 9876 9877 9988 9998 9999

CMD [ "sh", "prepare.sh"]
