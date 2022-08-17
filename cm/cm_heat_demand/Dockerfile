FROM ubuntu:20.04

# set timezone
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR cm-heat-demand

COPY cm_heat_demand/requirements.txt requirements.txt

# Note: if we install python3-gdal before the requirements, we are stuck with an old
# numpy version
RUN apt-get update && \
    apt-get install --yes \
        python3 \
        python3-pip \
        && \
    pip3 install -r requirements.txt && \
    apt-get install --yes \
        libgdal-dev \
        gdal-bin \
        python3-gdal \
        && \
    rm -rf /var/cache/apt/archives/

COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
COPY cm_heat_demand .
RUN python3 test.py
CMD ["python3", "worker.py"]
