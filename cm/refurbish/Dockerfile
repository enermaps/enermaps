FROM ubuntu:20.04

## ------------
## Set timezone
## ------------
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


## -------------------------
## Install required software
## -------------------------
RUN apt-get update \
    && apt-get --yes install \
    python3 \
    python3-pip \
    libgdal-dev \
    && rm -rf /var/cache/apt/archives/


## ----------------------
## Set main env variables
## ----------------------
ENV INPUT_DATA_DIR="/cm_inputs"
ENV CM_HDD_CDD_DIR="${INPUT_DATA_DIR}/hdd-cdd"
ENV CM_HDD_CDD_REPOSITORY="${INPUT_DATA_DIR}/hdd-cdd/hdd-cdd-main/data"
ENV CM_REFURBISH_DIR="${INPUT_DATA_DIR}/refurbish"
ENV POPGJSN="LAU_RG_01M_2020_4326.geojson"
ENV BUILSTK="building_stock.csv"
ENV TABULAX="tabula-umean.csv"

## print the main variables
RUN echo "/cm_input: ${INPUT_DATA_DIR}" \
    && echo "data repository: ${CM_HDD_CDD_REPOSITORY}"


## -------------------------
## Copy and install the code
## -------------------------
## choose the same name as the Docker service (by convention)
WORKDIR refurbish
COPY refurbish .
RUN pip3 install -r requirements.txt

COPY base /tmp/base
## the lines bellow where use to check that the we were using the latest version
## sometime the docker cache might create some issues, if it is the case use:
## docker-compose --file docker-compose-cm-test.yml build --no-cache cm-hdd_cdd
# RUN echo "-----" && head -n 50 /tmp/base/BaseCM/cm_hddcdd.py && echo "-----"
# RUN echo "-----" && head -n 50 /tmp/base/BaseCM/test_hddcdd.py && echo "-----"
RUN echo "-----\nInstalling BaseCM" \
    && cd /tmp/base && python3 setup.py install \
    && python3 test.py \
    && echo "-----\n"


## ---------------------------------
## Download required data and layers
## ---------------------------------
## by default use the python function to download the missing data
RUN python3 download.py

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
