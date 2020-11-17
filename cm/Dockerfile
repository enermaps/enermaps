FROM ubuntu:20.04
RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/
WORKDIR /cm
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN python3 test.py