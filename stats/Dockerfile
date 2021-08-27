FROM ubuntu:20.04

RUN apt-get update &&\
    apt-get --yes install python3 python3-pip cron &&\
    rm -rf /var/cache/apt/archives/


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY *.py /

CMD ["python3", "parseLog.py", "all"]
