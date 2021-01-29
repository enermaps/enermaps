FROM ubuntu:20.04
# SET TZ for GDAL
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/

RUN apt-get --yes install gdal-bin
RUN apt-get --yes install git

COPY . di
WORKDIR di

RUN pip3 install -r requirements.txt

RUN git clone --branch raster https://github.com/enermaps/datapackage-py.git
RUN cd datapackage-py && pip3 install -e .


RUN git clone --branch raster https://github.com/enermaps/dataflows.git
RUN cd dataflows && pip3 install -e .


CMD ["python3", "pipeline.py"]
