FROM ubuntu:20.04
RUN chmod 1777 /tmp # needed since July 2021 to be run on an Ubuntu 20.04.3 LTS server
RUN apt-get update &&\
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/


COPY ./requirements.txt stats/requirements.txt
RUN pip3 install -r stats/requirements.txt

COPY ./*.py stats/
COPY ./IP2LOCATION-LITE-DB1 stats/IP2LOCATION-LITE-DB1
WORKDIR stats
