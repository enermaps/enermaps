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
import utilities
from pandas_datapackage_reader import read_datapackage
import sqlalchemy as sqla
# Constants
logging.basicConfig(level=logging.INFO)

VALUE_VARS = ["public_ri_investment","private_ri_investment","inventions","public_ri_investment_eu_share","private_ri_investment_eu_share","inventions_eu_share","specialisation_index_inventions"]
ID_VARS = ["fid", "fields"]
ID = "index"
SPATIAL_VARS = ["country"]
UNIT = "MW"
ISRASTER = False

# In Docker
# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_USER = os.environ.get("DB_USER")
# DB_PASSWORD = os.environ.get("DB_PASSWORD")
# DB_DB = os.environ.get("DB_DB")

DB_HOST = "localhost"
DB_PORT = 5433
DB_USER = "test"
DB_PASSWORD = "example"
DB_DB = "dataset"


def FullCountryToCode(dbURL):
    db_engine = sqla.create_engine(dbURL)
    countries = pd.read_sql("SELECT * from public.spatial", db_engine)
    transl = countries

dbURL = "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                    DB_HOST=DB_HOST,
                    DB_PORT=DB_PORT,
                    DB_USER=DB_USER,
                    DB_PASSWORD=DB_PASSWORD,
                    DB_DB=DB_DB)
FullCountryToCode(dbURL)

def isValid(dp: frictionless.package.Package, new_dp: frictionless.package.Package):
    """

    Check whether the new DataPackage is valid and make sure the schema has not changed

    Parameters
    ----------
    dp : frictionless.package.Package
        Original datapackage 
    new_dp : frictionless.package.Package
        Datapackage describing the new loaded data

    Returns
    -------
    Boolean

    """
    val = frictionless.validate(new_dp)
    if (
        val["valid"]
        and dp["resources"][0]["schema"] == new_dp["resources"][0]["schema"]
    ):
        logging.info("Returning valid and schema-compliant data")
        return True
    else:
        logging.error("Data is not valid or the schema has changed")
        print(val)
        return False


def prepare(dp: frictionless.package.Package, name: str):
    """

    Prepare data in EnerMaps format

    Parameters
    ----------
    dp : frictionless.package.Package
        Valid datapackage 
    name : str
        Name of the dataset (used for constructing the FID)

    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    GeoDataFrame
        Spatial data in EnerMaps format.

    """
    data = read_datapackage(dp)
    data["fid"] = name + "_" + data[ID].astype(str)

    spatial = gpd.GeoDataFrame(
        data["fid"],
        columns=["fid"],
        geometry=gpd.points_from_xy(data.longitude, data.latitude),
        crs="EPSG:4326",
    )

    # Other fields to json
    def np_encoder(object):
        """Source: https://stackoverflow.com/a/65151218."""
        if isinstance(object, np.generic):
            return object.item()

    other_cols = [
        x for x in data.columns if x not in VALUE_VARS + SPATIAL_VARS + ID_VARS
    ]

    # Int64 to int
    data[other_cols].loc[:, data[other_cols].dtypes == "int64"] = (
        data[other_cols].loc[:, data[other_cols].dtypes == "int64"].astype(int)
    )
    data = data.replace({np.nan: None})
    data["fields"] = data[other_cols].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x, default=np_encoder))

    # Unpivoting
    data = data.melt(id_vars=["fid", "fields"], value_vars=VALUE_VARS)

    # Remove nan
    data = data.dropna()

    # Conversion
    enermaps_data = pd.DataFrame(
        columns=[
            "start_at",
            "fields",
            "variable",
            "value",
            "ds_id",
            "fid",
            "dt",
            "z",
            "israster",
            "unit",
        ]
    )

    enermaps_data["value"] = data["value"]
    enermaps_data["variable"] = data["variable"]
    enermaps_data["fields"] = data["fields"]
    enermaps_data["unit"] = UNIT
    enermaps_data["israster"] = ISRASTER

    return enermaps_data, spatial


def get(url: str, dp: frictionless.package.Package, force: bool = False):
    """

    Retrieve data and check update

    Parameters
    ----------
    url : str
        URL to retrieve the data from.
    dp : frictionless.package.Package
        Datapackage against which validating the data.
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
    ld = utilities.get_ld_json(url)
    csv_file = ld["distribution"][0]["contentUrl"]
    datePublished = ld["datePublished"]
    name = ld["name"].replace(" ", "_")

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")
    new_dp = frictionless.describe_package(csv_file, stats=True,)  # Add stats
    # Add date
    new_dp["datePublished"] = datePublished

    # Add missing valies
    new_dp.resources[0]["schema"]["missingValues"] = ["NULL"]
    for field in VALUE_VARS:
        new_dp.resources[0].schema.get_field(field).type = "number"

    # Logic for update
    if dp != None:  # Existing dataset
        # check stats
        isChangedStats = dp["resources"][0]["stats"] != new_dp["resources"][0]["stats"]
        isChangedDate = dp["datePublished"] != new_dp["datePublished"]

        if (
            isChangedStats or isChangedDate
        ):  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            if isValid(dp, new_dp):
                enermaps_data, spatial = prepare(new_dp, name)
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            if isValid(dp, new_dp):
                enermaps_data, spatial = prepare(new_dp, name)
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None, None
    else:  # New dataset
        dp = new_dp  # this is just for the sake of the schema control
        if isValid(dp, new_dp):
            enermaps_data, spatial = prepare(new_dp, name)

    return enermaps_data, spatial, new_dp


if __name__ == "__main__":
    argv = sys.argv
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_id = int(
        datasets[datasets["di_script"] == os.path.basename(argv[0])].index.values[0]
    )
    url = datasets.loc[
        datasets["di_script"] == os.path.basename(argv[0]), "di_URL"
    ].values[0]

    if "--force" in argv:
        isForced = True
    else:
        isForced = False
    dp = utilities.getDataPackage(
        ds_id,
        "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
            DB_HOST=DB_HOST,
            DB_PORT=DB_PORT,
            DB_USER=DB_USER,
            DB_PASSWORD=DB_PASSWORD,
            DB_DB=DB_DB,
        ),
    )

    data, spatial, dp = get(url=url, dp=dp, force=isForced)

    if isinstance(data, pd.DataFrame):
        # Remove existing dataset
        if utilities.datasetExists(
            ds_id,
            "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                DB_HOST=DB_HOST,
                DB_PORT=DB_PORT,
                DB_USER=DB_USER,
                DB_PASSWORD=DB_PASSWORD,
                DB_DB=DB_DB,
            ),
        ):
            utilities.removeDataset(
                ds_id,
                "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                    DB_HOST=DB_HOST,
                    DB_PORT=DB_PORT,
                    DB_USER=DB_USER,
                    DB_PASSWORD=DB_PASSWORD,
                    DB_DB=DB_DB,
                ),
            )
            logging.INFO("Removed existing dataset")

        # Create dataset table
        metadata = datasets.loc[ds_id].fillna("").to_dict()
        metadata["datapackage"] = dp
        metadata = json.dumps(metadata)
        dataset = pd.DataFrame([{"ds_id": ds_id, "metadata": metadata}])
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
        data["ds_id"] = ds_id
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
        spatial["ds_id"] = ds_id
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
