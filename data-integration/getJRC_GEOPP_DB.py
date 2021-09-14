#!/usr/bin/env python3
"""
Integrate JRC GEOPP DB into EnerMaps DB.
The original datapackage is used to retrieve the data.
This script allows for data updates.

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
import requests
import utilities
from pandas_datapackage_reader import read_datapackage

# Constants
logging.basicConfig(level=logging.INFO)

VALUE_VARS = ["gross_cap_ele", "ini_cap_ele", "gross_cap_th"]
ID_VARS = ["fid", "fields"]
ID = "id_powerplant"
SPATIAL_VARS = ["longitude", "latitude"]
UNIT = "MW"
ISRASTER = False
NAME = "JRC GEOPP"

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
    data.loc[:, other_cols].loc[:, data[other_cols].dtypes == "int64"] = (
        data.loc[:, other_cols].loc[:, data[other_cols].dtypes == "int64"].astype(int)
    )
    data = data.replace({np.nan: None})
    data["fields"] = data[other_cols].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x, default=np_encoder))

    # Unpivoting
    data = data.melt(id_vars=ID_VARS, value_vars=VALUE_VARS)

    # Remove nan
    data = data.dropna()

    # Conversion
    enermaps_data = utilities.ENERMAPS_DF
    enermaps_data["fid"] = data["fid"]
    enermaps_data["value"] = data["value"]
    enermaps_data["variable"] = data["variable"]
    enermaps_data["fields"] = data["fields"]
    enermaps_data["unit"] = UNIT
    enermaps_data["israster"] = ISRASTER

    return enermaps_data, spatial


def get(url: str, dp: frictionless.package.Package, force: bool = False):
    """

    Retrieve data and check update.

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
    ld = requests.get(url).json()
    csv_file = ld["@graph"][-1]["accessURL"]
    name = NAME

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")
    new_dp = frictionless.describe_package(csv_file, stats=True,)  # Add stats

    # Add missing valies
    new_dp.resources[0]["schema"]["missingValues"] = ["NULL"]
    for field in VALUE_VARS:
        new_dp.resources[0].schema.get_field(field).type = "number"

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        isChangedStats = dp["resources"][0]["stats"] != new_dp["resources"][0]["stats"]
        isChangedDate = False  # no date available

        if (
            isChangedStats or isChangedDate
        ):  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            if utilities.isDPvalid(dp, new_dp):
                enermaps_data, spatial = prepare(new_dp, name)
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            if utilities.isDPvalid(dp, new_dp):
                enermaps_data, spatial = prepare(new_dp, name)
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None, None
    else:  # New dataset
        dp = new_dp  # this is just for the sake of the schema control
        if utilities.isDPvalid(dp, new_dp):
            enermaps_data, spatial = prepare(new_dp, name)

    return enermaps_data, spatial, new_dp


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)
    url = datasets.loc[
        datasets["di_script"] == os.path.basename(sys.argv[0]), "di_URL"
    ].values[0]
    for ds_id in ds_ids:
        dp = utilities.getDataPackage(ds_id, DB_URL)

        data, spatial, dp = get(url=url, dp=dp, force=isForced)

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

            # Create spatial table
            spatial = spatial.to_crs("EPSG:3035")
            spatial["ds_id"] = ds_id
            utilities.toPostGIS(
                spatial, DB_URL, schema="spatial",
            )
