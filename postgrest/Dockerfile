FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="nointeractive" TZ="Europe/Zurich"

RUN  apt-get update \
  && apt-get install -y wget \
  && apt-get install -y xz-utils \
  && rm -rf /var/cache/apt/archives/


RUN wget https://github.com/PostgREST/postgrest/releases/download/v7.0.1/postgrest-v7.0.1-linux-x64-static.tar.xz
RUN tar xJf postgrest-v7.0.1-linux-x64-static.tar.xz
RUN rm postgrest-v7.0.1-linux-x64-static.tar.xz
COPY . .
#CMD ["sleep", "infinity"]
CMD ["./postgrest", "postgrest.conf"]
