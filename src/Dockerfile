# syntax=docker/dockerfile:1
FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 9876 9877 9998 9999

ADD . /usr/src/app/

#CMD ["sh", "prepare.sh"]
RUN sh prepare.sh

CMD [ "python", "main.py", "--config", "container", "--host=0.0.0.0"]
