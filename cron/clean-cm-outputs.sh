#!/bin/bash

# Load variables
export $(grep -v '^#' /etc/enermaps/config | xargs)

# Parse database logs
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose.yml exec api python3 /api/scripts/clean_cm_outputs.py
