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
import numpy as np
import pandas as pd
import utilities
from pandas_datapackage_reader import read_datapackage

# Constants
logging.basicConfig(level=logging.INFO)

VALUE_VARS = [
    "public_ri_investment",
    "private_ri_investment",
    "inventions",
    "public_ri_investment_eu_share",
    "private_ri_investment_eu_share",
    "inventions_eu_share",
    "specialisation_index_inventions",
]
ID_VARS = ["fid", "fields", "start_at"]
FORMAT = "%Y"
SPATIAL_VARS = ["country"]
TIME_VARS = ["year"]
UNIT = None
ISRASTER = False
DT = 8760

# In Docker
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")

DB_URL = "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
    DB_HOST=DB_HOST,
    DB_PORT=DB_PORT,
    DB_USER=DB_USER,
    DB_PASSWORD=DB_PASSWORD,
    DB_DB=DB_DB,
)


def getUnit(data: pd.DataFrame, schema: frictionless.schema.Schema):
    """
    Get unit from schema and assign it to the column.

    Parameters
    ----------
    data : pd.DataFrame
        Data in EnerMaps format.
    schema : frictionless.schema.Schema
        Schema of the data resource.

    Returns
    -------
    data : pd.DataFrame
        Data in EnerMaps format.

    """
    for variable in data.variable.unique():
        unit = schema.get_field(variable).get("unit")
        if unit == "decimal":
            data.loc[data["variable"] == variable, "unit"] = "%"
            data.loc[data["variable"] == variable, "value"] *= 100
        else:
            data.loc[data["variable"] == variable, "unit"] = unit
    return data


def isValid(dp: frictionless.package.Package, new_dp: frictionless.package.Package):
    """

    Check whether the new DataPackage is valid and make sure the schema has not changed.

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

    Prepare data in EnerMaps format.

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
    """
    data = read_datapackage(dp)

    # Encoding FID as country code
    data["fid"] = utilities.full_country_to_code(data[SPATIAL_VARS], DB_URL)

    # Other fields to json
    def np_encoder(object):
        """Source: https://stackoverflow.com/a/65151218."""
        if isinstance(object, np.generic):
            return object.item()

    other_cols = [
        x
        for x in data.columns
        if x not in VALUE_VARS + SPATIAL_VARS + ID_VARS + TIME_VARS
    ]

    # Int64 to int
    data.loc[:, other_cols].loc[:, data[other_cols].dtypes == "int64"] = (
        data.loc[:, other_cols].loc[:, data[other_cols].dtypes == "int64"].astype(int)
    )

    data = data.replace({np.nan: None})
    data["fields"] = data[other_cols].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x, default=np_encoder))
    data["start_at"] = pd.to_datetime(data[TIME_VARS[0]], format=FORMAT)

    # Unpivoting
    data = data.melt(id_vars=ID_VARS, value_vars=VALUE_VARS)
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
    enermaps_data["fid"] = data["fid"]
    enermaps_data["value"] = data["value"]
    enermaps_data["variable"] = data["variable"]
    enermaps_data["fields"] = data["fields"]
    enermaps_data["start_at"] = data["start_at"]
    enermaps_data["dt"] = DT
    enermaps_data["unit"] = UNIT
    enermaps_data["israster"] = ISRASTER

    enermaps_data = getUnit(enermaps_data, dp.resources[0].schema)

    return enermaps_data


def get(repository: str, dp: frictionless.package.Package, force: bool = False):
    """

    Retrieve data and check update.

    Parameters
    ----------
    repository : str
        URL of the Gitlab repository (raw).
    dp : frictionless.package.Package
        Datapackage against which validating the data.
    force : Boolean, optional
        If True, new data will be uploaded even if the same as in the db. The default is False.

    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    frictionless.package.Package
        Pakage descring the data.

    """
    new_dp = frictionless.Package(repository + "datapackage.json")

    # Make sure to read the csv file from remote
    new_dp.resources[0]["path"] = repository + new_dp.resources[0]["path"]
    new_dp.resources[0]["scheme"] = "https"

    isChangedStats = False  # initialize check

    datePublished = new_dp["datePublished"]
    name = new_dp["name"]

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")
    # Add date
    new_dp["datePublished"] = datePublished

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        isChangedStats = dp["resources"][0]["stats"] != new_dp["resources"][0]["stats"]
        isChangedDate = dp["datePublished"] != new_dp["datePublished"]

        if (
            isChangedStats or isChangedDate
        ):  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            if isValid(dp, new_dp):
                enermaps_data = prepare(new_dp, name)
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            if isValid(dp, new_dp):
                enermaps_data = prepare(new_dp, name)
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None, None
    else:  # New dataset
        dp = new_dp  # this is just for the sake of the schema control
        if isValid(dp, new_dp):
            enermaps_data = prepare(new_dp, name)

    return enermaps_data, new_dp


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
        isForced = True
    dp = utilities.getDataPackage(ds_id, DB_URL)

    data, dp = get(repository=url, dp=dp, force=isForced)

    if isinstance(data, pd.DataFrame):
        # Remove existing dataset
        if utilities.datasetExists(ds_id, DB_URL):
            utilities.removeDataset(ds_id, DB_URL)
            logging.info("Removed existing dataset")

        # Create dataset table
        metadata = datasets.loc[ds_id].fillna("").to_dict()
        metadata["datapackage"] = dp
        metadata = json.dumps(metadata)
        dataset = pd.DataFrame([{"ds_id": ds_id, "metadata": metadata}])
        utilities.toPostgreSQL(
            dataset, DB_URL, schema="datasets",
        )

        # Create data table
        data["ds_id"] = ds_id
        utilities.toPostgreSQL(
            data, DB_URL, schema="data",
        )
