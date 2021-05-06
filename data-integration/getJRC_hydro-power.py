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

# Constants

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

logging.basicConfig(level=logging.INFO)

UNPIVOTING_FIELDS = [
    "installed_capacity_MW",
    "pumping_MW",
    "storage_capacity_MWh",
    "avg_annual_generation_GWh",
]

VALUE_VARS = ["lat", "lon"]
SPATIAL_VARS = ["lat", "lon"]
ID = "id"


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
    GeoDataFrame
        Spatial data in EnerMaps format.

    """
    data = read_datapackage(dp)
    data["fid"] = name + "_" + data[ID].astype(str)

    data.set_index("fid", inplace=True)

    spatial = gpd.GeoDataFrame(
        data.index,
        geometry=gpd.points_from_xy(data[SPATIAL_VARS[1]], data[SPATIAL_VARS[0]]),
        crs="EPSG:4326",
    )
    spatial = spatial.to_crs("EPSG:3035")
    enermaps_data = data.melt(
        id_vars=data.columns[~data.columns.isin(UNPIVOTING_FIELDS)],
        value_vars=UNPIVOTING_FIELDS,
        ignore_index=False,
    )
    # Other fields to json
    enermaps_data = enermaps_data.replace({np.nan: None})

    def np_encoder(object):
        """
        Source: https://stackoverflow.com/a/65151218.
        """
        if isinstance(object, np.generic):
            return object.item()

    enermaps_data["fields"] = enermaps_data[
        data.columns[~data.columns.isin(UNPIVOTING_FIELDS)]
    ].to_dict(orient="records")
    enermaps_data["fields"] = enermaps_data["fields"].apply(
        lambda x: json.dumps(x, default=np_encoder)
    )
    enermaps_data = enermaps_data.drop(
        data.columns[~data.columns.isin(UNPIVOTING_FIELDS)], axis=1
    )
    enermaps_data = pd.merge(enermaps_data, data, on="fid")
    enermaps_data = enermaps_data.drop(data.columns, axis=1, errors="ignore")
    enermaps_data["unit"] = enermaps_data.variable.apply(lambda x: x.split("_")[-1])
    enermaps_data.reset_index(inplace=True)

    return enermaps_data, spatial


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
    name = new_dp["name"]

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")
    # Add date
    new_dp["datePublished"] = utilities.getGitHub(user, repo, "date")

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
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
