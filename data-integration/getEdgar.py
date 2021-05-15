#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 09:00:00 2021

Integrate JRC PPDB DB into EnerMaps DB

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
from getJRC_GEOPP_DB_csv import isValid
from pandas_datapackage_reader import read_datapackage

# Constants
logging.basicConfig(level=logging.INFO)

VALUE_VARS = ["Emissions"]
VARIABLE = "Emissions"
ID_VARS = ["fid", "fields"]
SPATIAL_VARS = ["Code"]
TIME_VARS = ["Year"]
UNIT = "Mt CO2/year"
DT = 8760
ID = "index"
ISRASTER = False
RESOURCE_IDX = 0
RESOURCE_NAME = "edgar-co2-emissions"

EXTRA_COUNTRIES = {
    "FRA_MCO": {"assigned": "FR", "disclaimer": "Includes emissions of Monaco."},
    "ISR_PSE": {
        "assigned": "IL",
        "disclaimer": "Includes data emissions of the State of Palestine.",
    },
    "ITA_SMR_VAT": {
        "assigned": "IT",
        "disclaimer": "Includes emissions of San Marino and The Holy See.",
    },
    "SRB_MNE": {"assigned": "RS", "disclaimer": "Includes emissions of Montenegro."},
    "ESP_AND": {"assigned": "ES", "disclaimer": "Includes emissions of Andorra."},
    "CHE_LIE": {"assigned": "CH", "disclaimer": "Includes emission of Liechtenstein."},
}

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


def get(url: str, dp: frictionless.package.Package, force: bool = False):
    """
    Retrieve data and check update.

    Parameters
    ----------
    url : str
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
    new_dp = frictionless.Package(url + "datapackage.json")

    # Make sure to read the csv file from remote
    new_dp.resources[RESOURCE_IDX]["path"] = url + new_dp.resources[0]["path"]
    new_dp.resources[RESOURCE_IDX]["scheme"] = "https"

    isChangedStats = False  # initialize check

    name = new_dp["name"]

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        if "stats" in dp["resources"][RESOURCE_IDX].keys():
            isChangedStats = (
                dp["resources"][RESOURCE_IDX]["stats"]
                != new_dp["resources"][RESOURCE_IDX]["stats"]
            )
        else:
            isChangedStats = False
        isChangedVersion = False  # no version
        if (
            isChangedStats or isChangedVersion
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
    GeoDataFrame
        Spatial data in EnerMaps format.

    """
    data = read_datapackage(dp, RESOURCE_NAME)

    # drop multindex
    data = data.reset_index()

    # Encoding FID as country code
    countries = read_datapackage("https://github.com/datasets/country-codes")
    alpha3_to_2 = dict(
        countries[["ISO3166-1-Alpha-3", "ISO3166-1-Alpha-2"]].to_dict(orient="split")[
            "data"
        ]
    )
    data["fid"] = data[SPATIAL_VARS].replace(alpha3_to_2)

    # Other fields to json
    def np_encoder(object):
        """Source: https://stackoverflow.com/a/65151218."""
        if isinstance(object, np.generic):
            return object.item()

    other_cols = [
        x for x in data.columns if x not in VALUE_VARS + SPATIAL_VARS + ID_VARS
    ]

    # Int64 to int
    data.loc[:, other_cols].loc[:, data[other_cols].dtypes == "int64"] = (
        data.loc[:, other_cols].loc[:, data[other_cols].dtypes == "int64"].astype(int)
    )
    data = data.replace({np.nan: None})
    data["fields"] = data[other_cols].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x, default=np_encoder))

    data["value"] = data[VALUE_VARS]
    data["variable"] = VARIABLE
    data["start_at"] = data[TIME_VARS].apply(lambda x: pd.to_datetime(x, format="%Y"))

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
    enermaps_data["dt"] = DT
    enermaps_data["start_at"] = data["start_at"]
    enermaps_data["value"] = data["value"]
    enermaps_data["variable"] = data["variable"]
    enermaps_data["fields"] = data["fields"]
    enermaps_data["unit"] = UNIT
    enermaps_data["israster"] = ISRASTER

    return enermaps_data


def postProcess(data: pd.DataFrame):
    """
    Coplete additional columns of the dataframe.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame in EnerMaps format.

    Returns
    -------
    data : pd.DataFrame
        DataFrame in EnerMaps format with completed fields.

    """

    def addDisclaimer(fields):
        fields["disclaimer"] = EXTRA_COUNTRIES[fid]["disclaimer"]
        return fields

    data["fields"] = data["fields"].apply(lambda x: json.loads(x))
    for fid in EXTRA_COUNTRIES.keys():
        data.loc[data.fid == fid, "fields"] = data.loc[data.fid == fid, "fields"].apply(
            addDisclaimer
        )
        data.loc[data.fid == fid, "fid"] = EXTRA_COUNTRIES[fid]["assigned"]
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x))
    return data


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
    dp = utilities.getDataPackage(ds_id, DB_URL)

    data, dp = get(url=url, dp=dp, force=isForced)

    if isinstance(data, pd.DataFrame):
        # Remove existing dataset
        if utilities.datasetExists(ds_id, DB_URL,):
            utilities.removeDataset(ds_id, DB_URL)
            logging.info("Removed existing dataset")

        # Postprocess
        data = postProcess(data)

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
