FROM ubuntu:20.04
RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/
COPY cm/cm_buildingload/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY cm/base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
COPY cm/cm_buildingload .
RUN mkdir -p tmp
RUN python3 test.py
CMD ["python3", "worker.py"]
