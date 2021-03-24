# Data integration for EnerMaps

This service retrieves the different sources to be integrated into the database.

## Available pipelines
At the moment the service does not run any command and stays active in the background.
You can manually execute the available pipelines witn the following commands:

  - 0: Admin units (LAU NUTS)
    `docker-compose exec data-integration python3 admin_units.py`

  - 31: HotMaps Geothermal potential
  	`docker-compose exec data-integration python3 getHotMaps_raster.py --select_ds_ids 31`

  - 2: JRC Geothermal power plants
  `docker-compose exec data-integration python3 getJRC_GEOPP_DB_csv.py`
  	

Reminder: you need to start both the db service (`docker-compose up -d db`) and the data-integration service (`docker-compose up -d data-integration`) before running the pipelines.
