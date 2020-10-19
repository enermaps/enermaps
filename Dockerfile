FROM ubuntu

ENV DEBIAN_FRONTEND="nointeractive" TZ="Europe/Zurich"
RUN apt update && apt install --yes python3-mapnik python3-pip

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 5000
ENTRYPOINT ["python3", "main.py"]