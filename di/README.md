# Data integration for EnerMaps

This service retrieves the different sources to be integrated into the database.

## Available pipelines

  - Admin units (LAU NUTS)
    `docker-compose run data-integration python3 admin_units.py`

  - NEWA data
  	`docker-compose run data-integration python3 getNEWA.py`


You need to start both the db service (`docker-compose up -d db`) and the data-integration service (`docker-compose run data-integration python3 getNEWA.py`) before running the pipelines.
