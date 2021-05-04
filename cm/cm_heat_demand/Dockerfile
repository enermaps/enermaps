FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="nointeractive" TZ="Europe/Zurich"
RUN apt update && apt install --yes \
    gdal-bin \
    python3-pip \
    python3-gdal && \
    rm -rf /var/cache/apt/archives/

WORKDIR cm-heat-demand

COPY cm_heat_demand/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
COPY cm_heat_demand .
RUN python3 test.py
CMD ["python3", "worker.py"]
