# Data integration for EnerMaps

This service retrieves the different sources to be integrated into the database.

## Available pipelines

At the moment the service does not run any command.
You can manually execute the available pipelines witn the following commands:

  - 0: Admin units (LAU NUTS)
    `docker-compose -f ../docker-compose-db.yml run data-integration admin_units.py`

  - 1: PVGIS raster files
    `docker-compose -f ../docker-compose-db.yml run data-integration getPVGIS.py`

  - 2: JRC Geothermal power plants
    `docker-compose -f ../docker-compose-db.yml run data-integration getJRC_GEOPP_DB_csv.py`

  - 3: JRC hydropower
    `docker-compose -f ../docker-compose-db.yml run data-integration getJRC-hydro-power.py`

  - 4: JRC PPDB
    `docker-compose -f ../docker-compose-db.yml run data-integration getJRC-PPDB-OPEN.py`

  - 5: EEA: Share of gross final consumption of renewable energy sources
    `docker-compose -f ../docker-compose-db.yml run data-integration getEEA.py`

  - 6: EUROSTAT Energy consumption in households
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 6`

  - 7: Electricity Map data
    `docker-compose -f ../docker-compose-db.yml run data-integration getElectricity.py`

  - 8: GISCO Population
    `docker-compose -f ../docker-compose-db.yml run data-integration getPopulation.py`

  - 9: EUROSTAT Degree Days
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 9`

  - 11: SETIS
    `docker-compose -f ../docker-compose-db.yml run data-integration getSETIS.py`

  - 14: Climate Extreme Indices,
    `docker-compose  -f ../docker-compose-db.yml run data-integration getPANGAEA.py`

  - 15: ERA5 reanalysis-era5-single-levels
    Note that the CDS API key is required. See [here](#cdsapirc).
    `docker-compose  -f ../docker-compose-db.yml run data-integration getEra5.py --select_ds_ids 15`

  - 16: EMHIRES: Wind power generation
    `docker-compose -f ../docker-compose-db.yml run data-integration getEMHIRES.py --select_ds_ids 16`

  - 17: EMHIRES: Solar power generation
    `docker-compose  -f ../docker-compose-db.yml run data-integration getEMHIRES.py --select_ds_ids 17`

  - 18: get Energy Efficiency indicator from energydata repository
    `docker-compose -f ../docker-compose-db.yml run data-integration getEnergydata.py`

  - 19: EDGAR CO₂ emissions
    `docker-compose -f ../docker-compose-db.yml run data-integration getEdgar.py`

  - 20: ERA5 reanalysis-era5-pressure-levels
    Note that the CDS API key is required. See [here](#cdsapirc).
    `docker-compose -f ../docker-compose-db.yml run data-integration getERA5.py --select_ds_ids 20`

  - 21: EU-DEM
    Note that the files must be manually downloaded by Copernicus website (requires log-in).
    Instructions are in the header of the Python file.
    `docker-compose -f ../docker-compose-db.yml run data-integration getESM-EUDEM.py --select_ds_ids 21`

  - 22: EUROSTAT Energy efficiency indicator
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 22`

  - 23: JRC Projected fresh water use from the European energy sector
    `docker-compose -f ../docker-compose-db.yml run data-integration getWater.py`

  - 24: Solar Atlas
    `docker-compose -f ../docker-compose-db.yml run data-integration getSolarAtlas.py`

  - 25: HotMaps wind potential
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_raster.py --select_ds_ids 25`

  - 27: S2BIOM
    `docker-compose -f ../docker-compose-db.yml run data-integration getS2BIOM.py`

  - 28: HotMaps Building stock analysis
    `docker-compose -f ../docker-compose-db.yml run data-integration getHotMaps_tabular.py`

  - 29: SET-Nav
    `docker-compose -f ../docker-compose-db.yml run data-integration getSET-Nav.py`

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

  - 46: OECD: Greenhouse gas emissions
    `docker-compose -f ../docker-compose-db.yml run data-integration getOECD.py`

  - 47: EUROSTAT Electricity prices for household consumers
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 47`

  - 48: EUROSTAT Expenditure per household on energy
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 48`

  - 49: EUROSTAT Energy dependence
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 49`

  - 50: EUROSTAT Regional GDP
    `docker-compose -f ../docker-compose-db.yml run data-integration getEurostat.py --select_ds_ids 50`

An additional pipeline can be used to add metadata for datasets that will only be listed in the OpenAIRE gateway:
    `docker-compose -f ../docker-compose-db.yml run data-integration not-in-EDMT.py`

Remember to start the db service via `docker-compose --file ../docker-compose-db.yml up -d db` before running the pipelines.

## Required files

### cdsapirc
The file `/data-integration/.cdsapirc` is required to build this service.
In order to execute data integration pipelines accessing the Copernicus Climate Data Store (`15` and `20`) the CDS API key should be provided.
You can find more information here on how to include the CDS API key in this file here:
https://cds.climate.copernicus.eu/api-how-to
If you are not interested in using these pipelines, an empty file should be created.
