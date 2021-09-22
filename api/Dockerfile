FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="nointeractive" TZ="Europe/Zurich"
RUN apt update && apt install --yes \
    gdal-bin \
    python3-mapnik \
    python3-pip \
    python3-gunicorn \
    gunicorn \
    libpq-dev \
    python3-gdal \
    cron && \
    rm -rf /var/cache/apt/archives/

WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

#always ensure the python test are fine before proceeding to build the image
RUN python3 test.py

EXPOSE 80
ENTRYPOINT scripts/entrypoint.sh
