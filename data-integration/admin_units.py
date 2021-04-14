#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:53:54 2020

@author: giuseppeperonato
"""

import logging
import os

import geopandas as gpd
import pandas as pd
import sqlalchemy as sqla
import utilities
from pyproj import CRS

# Constants
# GISCO datasets GEOJSON EPSG:4326 1:1milion
GISCO_DATASETS = {
    "countries": "https://gisco-services.ec.europa.eu/distribution/v2/countries/geojson/CNTR_RG_01M_2020_{}.geojson",
    "nuts": "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_{}.geojson",
    "lau": "https://gisco-services.ec.europa.eu/distribution/v2/lau/geojson/LAU_RG_01M_2019_{}.geojson",
}
# Dataset id
DS_ID = 0

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")


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

    admin_units.crs = crs.to_string()
    return admin_units


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    admin_units = get(GISCO_DATASETS, crs=CRS.from_epsg(3035))
    admin_units["ds_id"] = DS_ID
    dataset = pd.DataFrame([{"ds_id": DS_ID}])
    utilities.toPostgreSQL(
        dataset,
        "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
            DB_HOST=DB_HOST,
            DB_PORT=DB_PORT,
            DB_USER=DB_USER,
            DB_PASSWORD=DB_PASSWORD,
            DB_DB=DB_DB,
        ),
        schema="datasets",
    )
    utilities.toPostGIS(
        admin_units,
        "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
            DB_HOST=DB_HOST,
            DB_PORT=DB_PORT,
            DB_USER=DB_USER,
            DB_PASSWORD=DB_PASSWORD,
            DB_DB=DB_DB,
        ),
    )
