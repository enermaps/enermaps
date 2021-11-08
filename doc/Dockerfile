FROM ubuntu:18.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales locales-all
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y -q build-essential ruby-full python python-docutils ruby-bundler libicu-dev libreadline-dev libssl-dev zlib1g-dev git-core cmake tree && \
    apt-get clean && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# Install gollum and related libs
RUN gem install redcarpet github-markdown omniauth-github github-markup && \
    gem install gollum -v 4.1.4 && \
    gem install omnigollum -v 0.1.5

# gollum-data: Data for gollum patching
RUN mkdir /root/gollum-data
COPY src/gollum-data /root/gollum-data
WORKDIR /root

# Patch gollum for omnigollum
RUN export GEM_DIR=$(dirname "$(gem which gollum)")
RUN cp -r /root/gollum-data/gollum-patch/css/* "$(dirname "$(gem which gollum)")/gollum/public/gollum/css" && \
    cp -r /root/gollum-data/gollum-patch/js/* "$(dirname "$(gem which gollum)")/gollum/public/gollum/javascript" && \
    cp -r /root/gollum-data/gollum-patch/templates/* "$(dirname "$(gem which gollum)")/gollum/templates" && \
    cp -r /root/gollum-data/gollum-patch/views/* "$(dirname "$(gem which gollum)")/gollum/views"

# Copy scripts and make them executable
COPY src/scripts /root/scripts
RUN find /root/scripts -type f -exec chmod +x {} \;

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip

# docker-run: Setup for the startup & scheduled job-handler script
RUN mkdir /root/docker-run
COPY src/docker-run/requirements.txt /root/docker-run/requirements.txt
RUN pip3 install -r /root/docker-run/requirements.txt
COPY src/docker-run /root/docker-run

# Expose port 80, as Gollum needs it to serve the wiki
# Port is configured in /root/docker-run/run.py by the --port option
EXPOSE 80

# Handling git initialization and Gollum startup
# Using a Python script for the cleaner handling of environment variables and conditional operators
WORKDIR /root/docker-run
ENTRYPOINT ["python3", "-m", "app.run"]
