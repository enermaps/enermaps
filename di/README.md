# Data integration for EnerMaps

This service retrieves the different sources to be integrated into the database.

## Available pipelines

  - 0: Admin units (LAU NUTS)
    `docker-compose run data-integration python3 admin_units.py`

  - 25: NEWA data
  	`docker-compose run data-integration python3 getNEWA.py`

  - 2: JRC Geothermal power plants
  `docker-compose run data-integration python3 getJRC_GEOPP_DB_csv.py`
  	


You need to start both the db service (`docker-compose up -d db`) and the data-integration service (`docker-compose run data-integration python3 getNEWA.py`) before running the pipelines.
