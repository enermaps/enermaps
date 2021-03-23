#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:53:54 2020

@author: giuseppeperonato
"""

import geopandas as gpd
import pandas as pd
import sqlalchemy as sqla
import utilities
import logging

# GISCO datasets GEOJSON EPSG:4326 1:1milion
datasets = {
    "countries": "https://gisco-services.ec.europa.eu/distribution/v2/countries/geojson/CNTR_RG_01M_2020_{}.geojson",
    "nuts": "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_{}.geojson",
    "lau": "https://gisco-services.ec.europa.eu/distribution/v2/lau/geojson/LAU_RG_01M_2019_{}.geojson",
}

# Dataset id
ds_id = 0


def get(datasets: dict = datasets, crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
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
    source_crs_code = crs.split(":")[-1]
    logging.info("Downloading countries...")
    countries = gpd.read_file(datasets["countries"].format(source_crs_code), crs=crs)
    logging.info("Downloading NUTS...")
    nuts = gpd.read_file(datasets["nuts"].format(source_crs_code), crs=crs)
    logging.info("Downloading LAU...")
    lau = gpd.read_file(datasets["lau"].format(source_crs_code), crs=crs)
    logging.info("Done.")

    # Create consistent columns across ds
    lau = lau.rename({"LAU_NAME": "NAME"}, axis=1)
    lau["LEVL_CODE"] = 4

    nuts = nuts.rename({"NAME_LATN": "NAME"}, axis=1)

    countries = countries.rename({"CNTR_NAME": "NAME"}, axis=1)
    countries = countries.rename({"CNTR_ID": "CNTR_CODE"}, axis=1)
    countries["LEVL_CODE"] = 0

    # EU+ countries are included both in NUTS (level 0) and in "countries"
    # Discard then NUTS level 0
    nuts_noEU = nuts.loc[~nuts.id.isin(countries.id), :]

    admin_units = pd.concat([countries, nuts_noEU, lau], axis=0, ignore_index=True)

    admin_units = gpd.GeoDataFrame(
        admin_units.loc[
            :, ["FID", "NAME", "NAME_ENGL", "CNTR_CODE", "LEVL_CODE", "geometry"]
        ]
    )

    # New level codes
    admin_units.LEVL_CODE = admin_units.LEVL_CODE.replace(
        {0: "country", 1: "NUTS1", 2: "NUTS2", 3: "NUTS3", 4: "LAU"}
    )

    admin_units.crs = crs
    return admin_units


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    host = "db"
    port = 5432
    admin_units = get(datasets, crs="EPSG:3035")
    admin_units["ds_id"] = ds_id
    dataset = pd.DataFrame([{"ds_id": ds_id}])
    utilities.toPostgreSQL(
        dataset,
        "postgresql://test:example@{host}:{port}/dataset".format(host=host, port=port),
        schema="datasets",
    )
    utilities.toPostGIS(
        admin_units,
        "postgresql://test:example@{host}:{port}/dataset".format(host=host, port=port),
    )
