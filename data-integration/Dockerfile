FROM ubuntu:20.04
# SET TZ for GDAL
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    apt-get --yes install postgresql-client &&\
    apt-get --yes install gdal-bin &&\
    apt-get --yes install libgdal-dev &&\
    rm -rf /var/cache/apt/archives/

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt di/requirements.txt
WORKDIR di
RUN pip3 install -r requirements.txt

COPY . .

# Provisional command to keep the container alive
CMD ["sleep", "infinity"]

# Future pipeline, keep commented for now (=manual integration)
# CMD ["python3", "admin_units.py"]
# CMD ["python3", "getNEWA.py"]
