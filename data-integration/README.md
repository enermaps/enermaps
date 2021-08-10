# Data integration for EnerMaps

This service retrieves the different sources to be integrated into the database.

## Available pipelines

At the moment the service does not run any command.
You can manually execute the available pipelines witn the following commands:

  - 0: Admin units (LAU NUTS)
    `docker-compose -f ../docker-compose-db.yml run data-integration admin_units.py`

  - 2: JRC Geothermal power plants
    `docker-compose -f ../docker-compose-db.yml run data-integration getJRC_GEOPP_DB_csv.py`

  - 5: EEA: Share of gross final consumption of renewable energy sources
    `docker-compose -f ../docker-compose-db.yml run data-integration getEEA.py`

  - 7: Electricity Map data
    `docker-compose -f ../docker-compose-db.yml run data-integration getElectricity.py`

  - 19: EDGAR CO₂ emissions
    `docker-compose -f ../docker-compose-db.yml run data-integration getEdgar.py`

  - 30: Fuel consumption and technologies used in the heating/cooling sector
    `docker-compose -f ../docker-compose-db.yml run data-integration getENER.py`

  - 31: HotMaps Geothermal potential
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_raster.py --select_ds_ids 31`

  - 33: Building Height
  	Note that the files must be manually downloaded by Copernicus website (requires log-in).
  	Instructions are in the header of the Python file.
    `docker-compose -f ../docker-compose-db.yml run data-integration getBuildingHeight.py`

  - 43: HotMaps Heat Density
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_raster.py --select_ds_ids 43`

  - 45: HotMaps: Heated gross floor area density
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_raster.py --select_ds_ids 45`


Remember to start the db service via `docker-compose --file ../docker-compose-db.yml up -d db` before running the pipelines.
