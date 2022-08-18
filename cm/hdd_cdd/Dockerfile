FROM ubuntu:20.04

## -------------------------
## Setup common to all CMs
## -------------------------

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

## -------------------------
## Install required software
## -------------------------
RUN apt-get --yes install \
        libgdal-dev \
    && rm -rf /var/cache/apt/archives/

## ----------------------
## Set main env variables
## ----------------------
ENV INPUT_DATA_DIR="/cm_inputs"
ENV CM_HDD_CDD_DIR="${INPUT_DATA_DIR}/hdd-cdd"
ENV CM_HDD_CDD_REPOSITORY="${INPUT_DATA_DIR}/hdd-cdd/hdd-cdd-main/data"

## print the main variables
RUN echo "/cm_input: ${INPUT_DATA_DIR}" \
    && echo "data repository: ${CM_HDD_CDD_REPOSITORY}"

## -------------------------
## Copy and install the code
## -------------------------
## choose the same name as the Docker service (by convention)
WORKDIR hdd_cdd
COPY hdd_cdd .
RUN pip3 install -r requirements.txt

## ---------------------------------
## Download required data and layers
## ---------------------------------
## by default use the python function to download the missing data
RUN python3 download.py

## if you neet to check if you are using the latest version of the tests
## uncomment the following lines:
# RUN python3 -c "from pprint import pprint; \
#     from BaseCM import cm_hddcdd as hc; \
#     print('Public attributes of BaseCM.cm_hddcdd'); \
#     pprint([var for var in dir(hc) if not var.startswith('__')])"
# RUN python3 -c "from pprint import pprint; \
#     from BaseCM import test_hddcdd as hc; \
#     print('Public attributes of BaseCM.test_hddcdd'); \
#     pprint([var for var in dir(hc.TestCM) if var.startswith('test')])"

## To avoid to wait long docker build time it is possible to manually download the data
## from: https://gitlab.inf.unibz.it/URS/enermaps/hdd-cdd/-/archive/main/hdd-cdd-main.tar.gz
## extract the files and copy the `data`folder in `cm/hdd_cdd/` and then
## uncomment the next command:
# RUN mkdir -p /cm_inputs/hdd-cdd/hdd-cdd-main/ \
#     && cp -R data /cm_inputs/hdd-cdd/hdd-cdd-main/ \
#     && ls -l /cm_inputs/hdd-cdd/hdd-cdd-main/data/rcp45/cdd/26.0/monthly/average \
#     && rm -R data

## -----------------------------
## Generate the schema.json file
## -----------------------------
# extract from the data set the main parameters and save them on the schema.json
RUN python3 schema.py

## -------------
## Execute tests
## -------------
RUN python3 test.py

# activate the service
CMD ["python3", "worker.py"]
