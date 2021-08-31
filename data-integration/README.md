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

  - 6: EUROSTAT Energy consumption in households
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 6`

  - 7: Electricity Map data
    `docker-compose -f ../docker-compose-db.yml run data-integration getElectricity.py`

  - 8: GISCO Population
    `docker-compose -f ../docker-compose-db.yml run data-integration getPopulation.py`

  - 15: ERA5 reanalysis-era5-single-levels
    `docker-compose  -f ../docker-compose-db.yml run data-integration getERA5.py --select_ds_ids 15`

  - 19: EDGAR CO₂ emissions
    `docker-compose -f ../docker-compose-db.yml run data-integration getEdgar.py`

  - 20: ERA5 reanalysis-era5-pressure-levels
    `docker-compose run data-integration  -f ../docker-compose-db.yml getERA5.py --select_ds_ids 20`

  - 21: EU-DEM
    Note that the files must be manually downloaded by Copernicus website (requires log-in).
    Instructions are in the header of the Python file.
    `docker-compose -f ../docker-compose-db.yml run data-integration getESM-EUDEM.py --select_ds_ids 21`

  - 22: EUROSTAT Energy efficiency indicator
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 22`

  - 24: Solar Atlas
    `docker-compose -f ../docker-compose-db.yml run data-integration getSolarAtlas.py`

  - 28: HotMaps Building stock analysis
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_tabular.py`

  - 30: Fuel consumption and technologies used in the heating/cooling sector
    `docker-compose -f ../docker-compose-db.yml run data-integration getENER.py`

  - 31: HotMaps Geothermal potential
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_raster.py --select_ds_ids 31`

  - 33: Building Height
  	Note that the files must be manually downloaded by Copernicus website (requires log-in).
  	Instructions are in the header of the Python file.
    `docker-compose -f ../docker-compose-db.yml run data-integration getBuildingHeight.py`

  - 35: ESM
    Note that the files must be manually downloaded by Copernicus website (requires log-in).
    Instructions are in the header of the Python file.
    `docker-compose -f ../docker-compose-db.yml run data-integration getESM-EUDEM.py --select_ds_ids 35`

  - 42: EUROSTAT National Housing Census: type of living quarter by country
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 42`

  - 43: HotMaps Heat Density
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_raster.py --select_ds_ids 43`

  - 45: HotMaps: Heated gross floor area density
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_raster.py --select_ds_ids 45`

  - 47: EUROSTAT Electricity prices for household consumers
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 47`

  - 49: EUROSTAT Energy dependence
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 49`

  - 50: EUROSTAT Regional GDP
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 50`

Remember to start the db service via `docker-compose --file ../docker-compose-db.yml up -d db` before running the pipelines.

## Metadata table for OpenAIRE gateway

A table named `datasets_full` is used to provide metadata to the OpenAIRE Gateway, while waiting for the `datasets` table to be filled in with all pipelines.
Follow instructions on `addDatasets.py`.
