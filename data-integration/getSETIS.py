#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 09:00:00 2021

Integrate JRC GEOPP DB into EnerMaps DB

@author: giuseppeperonato
"""

import json
import logging
import os
import sys

import frictionless
import geopandas as gpd
import numpy as np
import pandas as pd
from pandas_datapackage_reader import read_datapackage

import utilities

# Constants
logging.basicConfig(level=logging.INFO)
DS_ID = 11
URL = "https://raw.githubusercontent.com/enermaps/datasets/main/SETIS/"
Force = False  # force integration if (meta)data has not changed

# In Docker
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")

DB_HOST = "localhost"
DB_PORT = 5433
DB_USER = "test"
DB_PASSWORD = "example"
DB_DB = "dataset"

def get(url: str, dp: frictionless.package.Package, force: bool = False):
    """

    Retrieve data and check validity/update.

    Parameters
    ----------
    URL : str
        URL to retrieve the data from.
    dp : frictionless.package.Package
        Datapackage agains which validating the data.
    force : Boolean, optional
        If True, new data will be uploaded even if the same as in the db. The default is False.

    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    GeoDataFrame
        Spatial data in EnerMaps format.
    frictionless.package.Package
        Pakage descring the data.

    """
    # Parsing
    value_vars = ["gross_cap_ele", "ini_cap_ele", "gross_cap_th"]
    id_vars = ["FID", "fields"]
    spatial_vars = ["longitude", "latitude"]

    new_dp = frictionless.Package(url + "datapackage.json")

    # Logic for update
    if dp != None: # Existing dataset
        # check stats
        ChangedStats = dp["resources"][0]["stats"] != new_dp["resources"][0]["stats"]
        ChangedDate = dp["datePublished"] != new_dp["datePublished"]

        if ChangedStats or ChangedDate: # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
        elif force: # Data integration will continue, even if data has not changed
            logging.info("Forced update")
        else: # Data integration will stop here, returning Nones
            logging.info(
                "Data has not changed. Use force update if you want to reupload."
            )
            return None, None, None
    else: # New dataset
        dp = new_dp # this is just for the sake of the schema control

    val = frictionless.validate(new_dp)
    
    # Make sure that the new dp is valid and that the schema has not changed
    if val["valid"] and dp["resources"][0]["schema"] == new_dp["resources"][0]["schema"]:
        logging.info("Returning valid and schema-compliant data")

        data = read_datapackage(new_dp)
        data["FID"] = name + "_" + data["id_powerplant"].astype(str)

        spatial = gpd.GeoDataFrame(
            data["FID"],
            columns=["FID"],
            geometry=gpd.points_from_xy(data.longitude, data.latitude),
            crs="EPSG:4326",
        )

        # Other fields to json
        def np_encoder(object):
            """Source: https://stackoverflow.com/a/65151218."""
            if isinstance(object, np.generic):
                return object.item()

        other_cols = [
            x for x in data.columns if x not in value_vars + spatial_vars + id_vars
        ]
        # Int64 to int
        data[other_cols].loc[:, data[other_cols].dtypes == "int64"] = (
            data[other_cols].loc[:, data[other_cols].dtypes == "int64"].astype(int)
        )
        data = data.replace({np.nan: None})
        data["fields"] = data[other_cols].to_dict(orient="records")
        data["fields"] = data["fields"].apply(
            lambda x: json.dumps(x, default=np_encoder)
        )

        # Unpivoting
        data = data.melt(id_vars=["FID", "fields"], value_vars=value_vars)

        # Remove nan
        data = data.dropna()

        # Conversion
        enermaps_data = pd.DataFrame(
            columns=[
                "time",
                "fields",
                "variable",
                "value",
                "ds_id",
                "FID",
                "dt",
                "z",
                "Raster",
                "unit",
            ]
        )

        enermaps_data["value"] = data["value"]
        enermaps_data["variable"] = data["variable"]
        enermaps_data["fields"] = data["fields"]
        # Constants
        enermaps_data["unit"] = "MW"
        enermaps_data["Raster"] = False
        return enermaps_data, spatial, new_dp
    else:
        logging.error("Data is not valid or the schema has changed")
        print(val)
        return None, None, None


if __name__ == "__main__":
    argv = sys.argv
    if "--force" in argv:
        Force = True
    dp = utilities.getDataPackage(
        DS_ID,
        "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
            DB_HOST=DB_HOST,
            DB_PORT=DB_PORT,
            DB_USER=DB_USER,
            DB_PASSWORD=DB_PASSWORD,
            DB_DB=DB_DB,
        ),
    )

    data, spatial, dp = get(url=URL, dp=dp, force=Force)

    if isinstance(data, pd.DataFrame):
        # Remove existing dataset
        if utilities.datasetExists(
            DS_ID,
            "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                DB_HOST=DB_HOST,
                DB_PORT=DB_PORT,
                DB_USER=DB_USER,
                DB_PASSWORD=DB_PASSWORD,
                DB_DB=DB_DB,
            ),
        ):
            utilities.removeDataset(
                DS_ID,
                "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                    DB_HOST=DB_HOST,
                    DB_PORT=DB_PORT,
                    DB_USER=DB_USER,
                    DB_PASSWORD=DB_PASSWORD,
                    DB_DB=DB_DB,
                ),
            )
            print("Removed existing dataset")

        # Create dataset table
        datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
        metadata = datasets.loc[DS_ID].fillna("").to_dict()
        metadata["datapackage"] = dp
        metadata = json.dumps(metadata)
        dataset = pd.DataFrame([{"ds_id": DS_ID, "metadata": metadata}])
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

        # Create data table
        data["ds_id"] = DS_ID
        utilities.toPostgreSQL(
            data,
            "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                DB_HOST=DB_HOST,
                DB_PORT=DB_PORT,
                DB_USER=DB_USER,
                DB_PASSWORD=DB_PASSWORD,
                DB_DB=DB_DB,
            ),
            schema="data",
        )

        # Create spatial table
        spatial = spatial.to_crs("EPSG:3035")
        spatial["ds_id"] = DS_ID
        utilities.toPostGIS(
            spatial,
            "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                DB_HOST=DB_HOST,
                DB_PORT=DB_PORT,
                DB_USER=DB_USER,
                DB_PASSWORD=DB_PASSWORD,
                DB_DB=DB_DB,
            ),
            schema="spatial",
        )
