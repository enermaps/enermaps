FROM ubuntu:20.04

# set timezone
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install --yes \
        python3-mapnik \
        python3-pip \
        python3-gunicorn \
        gunicorn \
        libpq-dev \
        gdal-bin \
        && \
    rm -rf /var/cache/apt/archives/

WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

#always ensure the python test are fine before proceeding to build the image
RUN python3 test.py

EXPOSE 80
CMD ["gunicorn", "--config", "gunicorn.py", "--bind", "0.0.0.0:80", "wsgi:app"]
