FROM ubuntu:20.04
RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/
WORKDIR cm-multiply
COPY example_multiply/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
COPY example_multiply .
RUN python3 test.py
CMD ["python3", "worker.py"]
