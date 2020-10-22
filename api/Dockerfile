FROM ubuntu

ENV DEBIAN_FRONTEND="nointeractive" TZ="Europe/Zurich"
RUN apt update && apt install --yes python3-mapnik python3-pip python3-gunicorn gunicorn python3-gdal

VOLUME /upload
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
#always ensure the python test are fine before proceeding to build the image
RUN python3 test.py

EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "wsgi:app"]
