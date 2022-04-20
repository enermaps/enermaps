FROM ubuntu:20.04

RUN chmod 1777 /tmp # needed since July 2021 to be run on an Ubuntu 20.04.3 LTS server
RUN apt-get update &&\
    apt-get --yes install python3 python3-pip git \
    postgresql-client

COPY requirements.txt /legends/requirements.txt
WORKDIR legends
RUN pip3 install -r requirements.txt

# what about .env file? Also, I must edit the code to deal with the new paths
COPY *.py /legends/
COPY *.csv /legends/

# Make pipelines executable
RUN chmod u+x *.py

# make subfolders readable and writable
RUN chmod -R u+rw *

#add the pipeline command in the path
ENV PATH="${PWD}:${PATH}"

# Future pipeline, keep commented for now (=manual integration)
# CMD ["python3", "load_legends.py"]
