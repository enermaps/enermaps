# Data integration for EnerMaps

This service retrieves the different sources to be integrated into the database.

## Available pipelines
At the moment the service does not run any command and stays active in the background.
You can manually execute the available pipelines witn the following commands:

  - 0: Admin units (LAU NUTS)
    `docker-compose exec data-integration python3 admin_units.py`

  - 25: NEWA data
  	`docker-compose exec data-integration python3 getNEWA.py`

  - 2: JRC Geothermal power plants
  `docker-compose exec data-integration python3 getJRC_GEOPP_DB_csv.py`
  	

Note: you need to start both the db service (`docker-compose up -d db`) and the data-integration service (`docker-compose up -d data-integration`) before running the pipelines.
