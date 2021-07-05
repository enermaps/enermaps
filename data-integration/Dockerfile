FROM ubuntu:20.04
# SET TZ for GDAL
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update &&\
    apt-get --yes install python3 python3-pip git \
    postgresql-client \
    gdal-bin \
    proj-bin \
    libgdal-dev &&\
    rm -rf /var/cache/apt/archives/


ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt /data-integration/requirements.txt
WORKDIR data-integration
RUN pip3 install -r requirements.txt

# PROVISIONAL: Installed a forked version of pandas-datapackage-reader
RUN git clone https://github.com/enermaps/pandas-datapackage-reader.git && \
    cd pandas-datapackage-reader && \
    pip3 install -e .

COPY *.py /data-integration/
COPY *.csv /data-integration/

#add the pipeline command in the path
ENV PATH="${PWD}:${PATH}"

# Future pipeline, keep commented for now (=manual integration)
# CMD ["python3", "admin_units.py"]
# CMD ["python3", "getHotMaps_raster.py"]
