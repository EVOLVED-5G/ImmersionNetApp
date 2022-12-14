# syntax=docker/dockerfile:1
FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y jq && apt-get clean

ADD . /usr/src/app/

EXPOSE 9876 9877 9988 9998 9999

# Version without deployment, just a container
#CMD [ "sh", "prepare.sh"]
#Version for Malaga deployment
CMD [ "sh", "prepare_deploy.sh"]
