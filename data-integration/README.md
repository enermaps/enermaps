# Data integration for EnerMaps

This service retrieves the different sources to be integrated into the database.

## Available pipelines

At the moment the service does not run any command and stays active in the background.
You can manually execute the available pipelines witn the following commands:

  - 0: Admin units (LAU NUTS)
    `docker-compose run data-integration admin_units.py`

  - 2: JRC Geothermal power plants
    `docker-compose run data-integration getJRC_GEOPP_DB_csv.py`

  - 43: HotMaps Heat Density
    `docker-compose run data-integration getHotMaps_raster.py --select-ds-ids 43`

you need to start both the db service via `docker-compose up -d db`) before running the pipelines.
