#!/usr/bin/env python3
"""
Obtain GISCO admin units that will be loaded as ds_id = 0.
No update check is performed here.

@author: giuseppeperonato
"""

import json
import logging
import os
import sys

import geopandas as gpd
import pandas as pd
from pyproj import CRS

import utilities

# GISCO datasets GEOJSON EPSG:4326 1:1milion
GISCO_DATASETS = {
    "countries": "https://gisco-services.ec.europa.eu/distribution/v2/countries/geojson/CNTR_RG_01M_2020_{}.geojson",
    "nuts": "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_{}.geojson",
    "lau": "https://gisco-services.ec.europa.eu/distribution/v2/lau/geojson/LAU_RG_01M_2019_{}.geojson",
}
logging.basicConfig(level=logging.INFO)

DS_ID = 0

METADATA = {"parameters": {"is_raster": False}, "default_parameters": {}}

DB_URL = utilities.DB_URL


def get(
    datasets: dict = GISCO_DATASETS, crs: CRS = CRS.from_epsg(3035)
) -> gpd.GeoDataFrame:
    """
    Retrieve NUTS, LAU and countries from GISCO API and make a single, consistent GDF.

    Parameters
    ----------
    datasets : dict
        dict with API URLs.
    crs : str, optional
        Spatial Reference System. The default is "EPSG:4326".

    Returns
    -------
    admin_units : GeoDataFrame
        Table with all administrative units.

    """
    source_crs_code = crs.to_epsg()
    logging.info("Downloading countries...")
    countries = gpd.read_file(
        datasets["countries"].format(source_crs_code), crs=crs.to_string()
    )
    logging.info("Downloading NUTS...")
    nuts = gpd.read_file(datasets["nuts"].format(source_crs_code), crs=crs.to_string())
    logging.info("Downloading LAU...")
    lau = gpd.read_file(datasets["lau"].format(source_crs_code), crs=crs.to_string())
    logging.info("Done.")

    # Convert to lower case
    countries.columns = countries.columns.str.lower()
    nuts.columns = nuts.columns.str.lower()
    lau.columns = lau.columns.str.lower()

    # Create consistent columns across ds
    lau = lau.rename({"lau_name": "name"}, axis=1)
    lau["levl_code"] = 4

    nuts = nuts.rename({"name_latn": "name"}, axis=1)

    countries = countries.rename({"cntr_name": "name"}, axis=1)
    countries = countries.rename({"cntr_id": "cntr_code"}, axis=1)
    countries["levl_code"] = 0

    # EU+ countries are included both in NUTS (level 0) and in "countries"
    # Discard then NUTS level 0
    nuts_noEU = nuts.loc[~nuts.id.isin(countries.id), :]

    admin_units = pd.concat([countries, nuts_noEU, lau], axis=0, ignore_index=True)

    admin_units = gpd.GeoDataFrame(
        admin_units.loc[
            :, ["fid", "name", "name_engl", "cntr_code", "levl_code", "geometry"]
        ]
    )

    # New level codes
    admin_units.levl_code = admin_units.levl_code.replace(
        {0: "country", 1: "NUTS1", 2: "NUTS2", 3: "NUTS3", 4: "LAU"}
    )

    # Convert to ISO 3166-1 alpha-2
    transl = {"UK": "GB", "EL": "GR"}
    admin_units["fid"] = admin_units["fid"].replace(transl)
    admin_units["cntr_code"] = admin_units["cntr_code"].replace(transl)

    admin_units.crs = crs.to_string()
    return admin_units


def integrate(enermaps_spatial: gpd.GeoDataFrame):
    """Integrate datasets. Each (Geo)DataFrame corresponds to a SQL table."""
    # Upload dataset record
    enermaps_datasets = pd.DataFrame(
        [
            {
                "ds_id": DS_ID,
                "metadata": json.dumps(METADATA),
                "shared_id": "nuts-lau",
            }
        ]
    )
    utilities.toPostgreSQL(
        enermaps_datasets,
        DB_URL,
        schema="datasets",
    )
    # Upload spatial records
    enermaps_spatial["ds_id"] = DS_ID
    utilities.toPostGIS(enermaps_spatial, DB_URL)

    # Upload empty data records
    enermaps_data = enermaps_spatial.loc[:, ["ds_id", "fid"]].copy()
    enermaps_data["value"] = 0
    enermaps_data["variable"] = ""
    utilities.toPostgreSQL(
        enermaps_data,
        DB_URL,
        schema="data",
    )


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)

    if utilities.datasetExists(DS_ID, DB_URL):
        if isForced:
            utilities.removeDataset(DS_ID, DB_URL)
            logging.info("Removed existing dataset")
            enermaps_spatial = get()
            integrate(enermaps_spatial)
        else:
            logging.info("The dataset already exists. Use --force to replace it.")
    else:
        enermaps_spatial = get()
        integrate(enermaps_spatial)
