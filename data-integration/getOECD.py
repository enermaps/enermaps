#!/usr/bin/env python3
"""
Get OECD data.

Using the API instead of pandasdmx, as the datastructure is not directly retrievable by it.
Data is already unpivoted.
We create a datapackage preserving the data stats, whose change is used to trigger an update.

@author: giuseppeperonato
"""
import json
import logging
import os
import sys
import urllib

import frictionless
import numpy as np
import pandas as pd
import utilities
from pandas_datapackage_reader import read_datapackage
from utilities import download_url

# Constants
FIELDS = ["Pollutant"]
VARS = ["Variable", "Pollutant"]
VALUES = ["Value"]
UNITS = ["Unit", "PowerCode"]
TIME_VARS = ["YEA"]
TIME_FORMAT = "%Y"
SPATIAL_VARS = ["COU"]
DT = 8760
ISRASTER = False

logging.basicConfig(level=logging.INFO)

DB_URL = utilities.DB_URL


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
    data = read_datapackage(dp)

    # Other fields to json
    def np_encoder(object):
        """Source: https://stackoverflow.com/a/65151218."""
        if isinstance(object, np.generic):
            return object.item()

    data["fields"] = data[FIELDS].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x, default=np_encoder))

    # Encoding FID as country code
    countries = read_datapackage("https://github.com/datasets/country-codes")
    alpha3_to_2 = dict(
        countries[["ISO3166-1-Alpha-3", "ISO3166-1-Alpha-2"]].to_dict(orient="split")[
            "data"
        ]
    )
    data["fid"] = data[SPATIAL_VARS].replace(alpha3_to_2)

    # Conversion
    enermaps_data = utilities.ENERMAPS_DF
    enermaps_data["fid"] = data["fid"]
    enermaps_data["start_at"] = data[TIME_VARS].apply(
        lambda x: pd.to_datetime(x, format=TIME_FORMAT)
    )
    enermaps_data["value"] = data[VALUES]
    enermaps_data["variable"] = data[VARS].agg(" | ".join, axis=1)
    enermaps_data["fields"] = data["fields"]
    enermaps_data["unit"] = data[UNITS].agg(" | ".join, axis=1)
    enermaps_data["dt"] = DT
    enermaps_data["israster"] = ISRASTER

    return enermaps_data


def get(url, dp, name="", force=False):
    """
    Retrieve data.

    Parameters
    ----------
    url : str
        URL to retrieve the data from.
    dp : frictionless.package
        Datapackage agains which validating the data.
    name : str, optional
        Name of the dataset.
    force : Boolean, optional
        If True, new data will be uploaded even if the same as in the db. The default is False.

    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    frictionless.package
        Pakage descring the data.

    """
    download_url(url, "{}.csv".format(name))

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")
    new_dp = frictionless.describe_package("{}.csv".format(name), stats=True)
    new_dp.resources[0]["path"] = os.path.join("{}.csv".format(name))

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        isChangedStats = dp["resources"][0]["stats"] != new_dp["resources"][0]["stats"]
        if "datePublished" in dp.keys():
            isChangedDate = dp["datePublished"] != new_dp["datePublished"]
        else:
            isChangedDate = False
        if (
            isChangedStats or isChangedDate
        ):  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            if utilities.isDPvalid(dp, new_dp):
                enermaps_data = prepare(new_dp, name)
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            if utilities.isDPvalid(dp, new_dp):
                enermaps_data = prepare(new_dp, name)
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None
    else:  # New dataset
        dp = new_dp  # this is just for the sake of the schema control
        if utilities.isDPvalid(dp, new_dp):
            enermaps_data = prepare(new_dp, name)

    # Removing downloaded_file
    if os.path.exists("{}.csv".format(name)):
        os.remove("{}.csv".format(name))

    return enermaps_data, new_dp


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)
    url = datasets.loc[
        datasets["di_script"] == os.path.basename(sys.argv[0]), "di_URL"
    ].values[0]

    # Get name of dataset
    name = urllib.parse.quote_plus(
        datasets.loc[
            datasets["di_script"] == os.path.basename(sys.argv[0]), "Title",
        ].values[0]
    )
    for ds_id in ds_ids:
        dp = utilities.getDataPackage(ds_id, DB_URL)

        data, dp = get(url=url, dp=dp, name=name, force=isForced)

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
