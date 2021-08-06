#!/usr/bin/env python3
"""
Import the Hotmaps tabular datasets.
The original datapackage is used to retrieve the data.
This script allows for data updates.

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

OTHER_FIELDS = ["sector", "subsector", "btype", "bage", "detail", "estimated", "source"]
VARIABLE = ["topic", "feature", "type"]
UNIT = ["unit"]
TIME = ["unit"]
VALUE = ["value"]
SPATIAL = ["country_code"]
ISRASTER = False
TIME = ["bage"]
TIME_TRANSL = {
    "Before 1945": None,
    "1945 - 1969": pd.to_datetime(1945, format="%Y"),
    "1970 - 1979": pd.to_datetime(1970, format="%Y"),
    "1980 - 1989": pd.to_datetime(1980, format="%Y"),
    "1990 - 1999": pd.to_datetime(1990, format="%Y"),
    "2000 - 2010": pd.to_datetime(2000, format="%Y"),
    "Post 2010": pd.to_datetime(2011, format="%Y"),
    "Berfore 1945": None,
}

DB_URL = utilities.DB_URL


def prepare(dp: frictionless.package.Package):
    """

    Prepare data in EnerMaps format.

    Parameters
    ----------
    dp : frictionless.package.Package
        Valid datapackage

    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    GeoDataFrame
        Spatial data in EnerMaps format.

    """
    data = read_datapackage(dp)

    data["estimated"] = data["estimated"] == 1

    enermaps_data = utilities.ENERMAPS_DF
    data = data.where(data.notnull(), None)

    # Other fields to json
    def np_encoder(object):
        """Source: https://stackoverflow.com/a/65151218."""
        if isinstance(object, np.generic):
            return object.item()

    enermaps_data["fields"] = data[OTHER_FIELDS].to_dict(orient="records")
    enermaps_data["fields"] = enermaps_data["fields"].apply(
        lambda x: json.dumps(x, default=np_encoder)
    )

    enermaps_data["fid"] = data[SPATIAL]
    enermaps_data["unit"] = data[UNIT]
    enermaps_data["variable"] = data[VARIABLE].astype(str).agg(" | ".join, axis=1)
    enermaps_data["israster"] = ISRASTER
    enermaps_data["value"] = data[VALUE]
    enermaps_data["start_at"] = data[TIME]
    enermaps_data["start_at"] = enermaps_data["start_at"].replace(TIME_TRANSL)

    return enermaps_data


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
    user, repo = url.split("/")[3:5]

    # Make sure to read the csv file from remote
    new_dp.resources[0]["path"] = url + new_dp.resources[0]["path"]
    new_dp.resources[0]["scheme"] = "https"

    isChangedStats = False  # initialize check

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        isChangedVersion = dp["version"] != new_dp["version"]

        if (
            isChangedStats or isChangedVersion
        ):  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            if isValid(dp, new_dp):
                enermaps_data = prepare(new_dp)
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            if isValid(dp, new_dp):
                enermaps_data = prepare(new_dp)
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None, None
    else:  # New dataset
        dp = new_dp  # this is just for the sake of the schema control
        if isValid(dp, new_dp):
            enermaps_data = prepare(new_dp)

    return enermaps_data, new_dp


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)

    for ds_id in ds_ids:
        logging.info("Retrieving Dataset {}".format(ds_id))
        url = datasets.loc[ds_id, "di_URL"]
        dp = utilities.getDataPackage(ds_id, DB_URL)

        data, dp = get(url=url, dp=dp, force=isForced)

        if isinstance(data, pd.DataFrame):
            # Remove existing dataset
            if utilities.datasetExists(ds_id, DB_URL,):
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
