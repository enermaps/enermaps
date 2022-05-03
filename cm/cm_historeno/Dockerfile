FROM ubuntu:20.04

# set env variable
ENV HOST_DIR=cm_historeno
ENV DOCKER_DIR=cm-historeno

# set timezone
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get --yes install \
        python3 \
        python3-pip \
        libgdal-dev \
        && \
    rm -rf /var/cache/apt/archives/

# choose the same name as the Docker service (by convention)
WORKDIR $DOCKER_DIR

# replace [example_empty] by your CM folder name
COPY $HOST_DIR/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
# replace [example_empty] by your CM folder name
COPY $HOST_DIR .
RUN python3 test.py
CMD ["python3", "worker.py"]
