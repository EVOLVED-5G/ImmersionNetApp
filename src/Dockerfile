# syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /usr/src/app
RUN mkdir -p capif_onboarding

ADD requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt
# RUN pip3 install git+https://github.com/EVOLVED-5G/SDK-CLI.git@develop

RUN apt-get update && apt-get install -y jq && apt-get clean

ADD . /usr/src/app/

EXPOSE 9876 9877 9988 9998 9999

# Version without deployment, just a container
#CMD [ "sh", "prepare.sh"]
#Version for Malaga deployment
CMD [ "sh", "prepare_deploy.sh"]
