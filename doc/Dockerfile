FROM ubuntu:20.04

# Prevent interactive installtion of packages
ARG DEBIAN_FRONTEND=noninteractive

# Handle locales
RUN apt-get update && apt-get install -y locales locales-all
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Base dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y -q build-essential \
                          ruby-full ruby-bundler \
                          libicu-dev libreadline-dev libssl-dev zlib1g-dev  \
                          git-core cmake pkg-config  \
                          python3 python3-pip python3-docutils && \
    apt-get clean && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# Equivalent to ~/app, as referenced in config.rb
WORKDIR /root/app

# Install Ruby dependencies
COPY ./src/gollum/Gemfile ./gollum/Gemfile
RUN cd gollum && bundle install

# Install Python dependencies
COPY ./src/docker-run/requirements.txt ./docker-run/requirements.txt
RUN pip3 install -r ./docker-run/requirements.txt

# Copy the gollum-specific files
COPY ./src/gollum ./gollum
# Copy the customized files to the gollum gem's dirs
RUN cp -r ./gollum/views/* "$(dirname "$(gem which gollum)")/gollum/views" && \
    cp -r ./gollum/templates/* "$(dirname "$(gem which gollum)")/gollum/templates"

# Copy the python-specific files
COPY ./src/docker-run ./docker-run

# Copy scripts and make them executable
COPY ./src/scripts ./scripts
RUN find ./scripts -type f -exec chmod +x {} \;

# Expose port 80, as Gollum needs it to serve the wiki
# Port is configured in /root/app/docker-run/run.py by the --port option
EXPOSE 80

# Handling git initialization and Gollum startup
# Using a Python script for the cleaner handling of environment variables and conditional operators
WORKDIR /root/app/docker-run
ENTRYPOINT ["python3", "-m", "app.run"]
