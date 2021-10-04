#!/bin/bash

# Load variables
export $(grep -v '^#' /etc/enermaps/config | xargs)

# Parse database logs
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm stats python3 parseLog.py all
