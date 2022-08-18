FROM ubuntu:20.04

# set timezone
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Python
RUN apt-get update && \
    apt-get --yes install \
        python3 \
        python3-pip \
        && \
    rm -rf /var/cache/apt/archives/

# Install the base library for CMs
COPY base /tmp/base
RUN cd /tmp/base && \
    pip3 install . && \
    python3 test.py

# Install additional dependencies (note: we do it after the above steps to take advantage of the cache during builds)
RUN apt-get install --yes \
        libgdal-dev \
        gdal-bin \
        libpq-dev \
        && \
    rm -rf /var/cache/apt/archives/

# Install this CM specific files
WORKDIR cm-dhexppot
COPY cm_dhexppot .
RUN pip3 install -r requirements.txt
RUN mkdir -p tmp
RUN python3 test.py
CMD ["python3", "worker.py"]
