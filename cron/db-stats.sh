#!/bin/bash
# Load variables
export $(grep -v '^#' ~/.enermaps | xargs)

# Parse database logs
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run stats python3 parseLog.py all
