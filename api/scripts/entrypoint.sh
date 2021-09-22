#!/bin/bash

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

# Setup a cron job
echo "SHELL=/bin/bash
BASH_ENV=/container.env
*/5 * * * * root python3 /api/scripts/clean_cm_outputs.py
" > /etc/cron.d/clean_cm_outputs

service cron start

# Start the web server
gunicorn --config gunicorn.py --bind 0.0.0.0:80 wsgi:app
