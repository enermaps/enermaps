FROM ubuntu:20.04
# SET TZ for GDAL
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/
# choose the same name as the Docker service (by convention)
WORKDIR cm-geofile
# replace [example_empty] by your CM folder name
COPY example_empty/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# COPY multiply/gcs.csv /usr/local/lib/python3.8/dist-packages/rasterio/gdal_data/gcs.csv
COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
# replace [example_empty] by your CM folder name
COPY example_empty .
RUN python3 test.py
CMD ["python3", "worker.py"]
