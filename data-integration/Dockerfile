FROM ubuntu:20.04
# SET TZ for GDAL
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update &&\
    apt-get --yes install python3 python3-pip \
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
RUN apt-get --yes install git
RUN git clone https://github.com/enermaps/pandas-datapackage-reader.git
RUN cd pandas-datapackage-reader && pip3 install -e .

COPY *.py /data-integration/
COPY *.csv /data-integration/

# Provisional command to keep the container alive
CMD ["sleep", "infinity"]

# Future pipeline, keep commented for now (=manual integration)
# CMD ["python3", "admin_units.py"]
# CMD ["python3", "getHotMaps_raster.py"]
