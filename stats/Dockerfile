FROM ubuntu:20.04

RUN apt-get update &&\
    apt-get --yes install python3 python3-pip cron &&\
    rm -rf /var/cache/apt/archives/


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY *.py /

# Copy hello-cron file to the cron.d directory
COPY cronjobs /etc/cron.d/cronjobs

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cronjobs

# Apply cron job
RUN crontab /etc/cron.d/cronjobs

CMD ["cron", "-f"]
