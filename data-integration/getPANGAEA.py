#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 22:07:47 2021

@author: giuseppeperonato
"""


import argparse
import json
import logging
import os
import sys
from pyproj import CRS
import frictionless
import pandas as pd
import utilities

# Constants
logging.basicConfig(level=logging.INFO)
Z = None
DT = 720
SEL = "MON"
EPSG = 4326

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


def prepare(new_dp):
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    for resource_idx,resource in enumerate(dp["resources"]):
        file = "https://doi.pangaea.de/10.1594/PANGAEA.898014?format=textfile"
        r = requests.get(file,stream=True)
        lines = [line for line in r.iter_lines()]
        skiprows = [ind for ind, i in enumerate(lines) if i.startswith(b'*/')][0]
        files = pd.read_csv(file,skiprows=skiprows+1,delimiter="\t")
        
        files = files.loc[files["File name"].str.contains(SEL),:]
        
        # Prepare df containing paths to rasters
        rasters = []
        for r, row in files.iterrows():
            if not os.path.exists(os.path.join("tmp",row["File name"])):
                utilities.download_url(row["URL file"],os.path.join("tmp",row["File name"]))
            raster = {
                "value": os.path.join("tmp",row["File name"]),
                "start_at": pd.to_datetime(row["File name"].split("_")[6]),
                "z": None,
                "unit": None,
                "dt": DT,
                "crs": CRS.from_epsg(EPSG),
                "variable": row["File name"].split("_")[0]
            }
            rasters.append(raster)
            if dp != None and "stats" in new_dp["resources"][resource_idx]:
                    if (
                        dp["resources"][resource_idx]["stats"]
                        != new_dp["resources"][resource_idx]["stats"]
                    ):
                        isChangedStats = True
        rasters = pd.DataFrame(rasters)
    isChangedVersion = dp["version"] != new_dp["version"]
    if isChangedStats or isChangedVersion:
        logging.info("Data has changed")
        data_enermaps = utilities.prepareRaster(rasters, delete_orig=True)
    elif isForced:
        logging.info("Forced update")
        data_enermaps = utilities.prepareRaster(rasters, delete_orig=True)
    else:
        logging.info("Data has not changed. Use --force if you want to reupload.")
        return None, None
    else:  # New dataset
        data_enermaps = utilities.prepareRaster(rasters, delete_orig=True)

        

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
    ld = utilities.get_ld_json(url)
    for resource in ld["distribution"]:
        if resource["@type"] == "DataDownload":
            if resource["encodingFormat"] == 'CSV' or resource["encodingFormat"] == 'text/tab-separated-values':
                file =  resource['contentUrl']
    datePublished = ld["datePublished"]
    name = ld["name"].replace(" ", "_")

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")
    new_dp = frictionless.describe_package(
        file,
        stats=True,
    )  # Add stats
    # Add date
    new_dp["datePublished"] = datePublished
    
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
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_ids = datasets[datasets["di_script"] == os.path.basename(sys.argv[0])].index
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Import HotMaps raster")
        parser.add_argument("--force", action="store_const", const=True, default=False)
        parser.add_argument(
            "--select_ds_ids", action="extend", nargs="+", type=int, default=[]
        )
        args = parser.parse_args()
        isForced = args.force
        if len(args.select_ds_ids) > 0:
            ds_ids = args.select_ds_ids
    else:
        isForced = False

    for ds_id in ds_ids:
        logging.info("Retrieving Dataset {}".format(ds_id))
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

        data, dp = get(datasets.loc[ds_id, "di_URL"], dp, isForced)

        if isinstance(data, pd.DataFrame):
            if utilities.datasetExists(
                ds_id,
                DB_URL,
            ):
                utilities.removeDataset(ds_id, DB_URL)
                logging.info("Removed existing dataset")

            # Create dataset table
            metadata = datasets.loc[ds_id].fillna("").to_dict()
            metadata["datapackage"] = dp
            metadata = json.dumps(metadata)
            dataset = pd.DataFrame([{"ds_id": ds_id, "metadata": metadata}])
            utilities.toPostgreSQL(
                dataset,
                DB_URL,
                schema="datasets",
            )

            # Create data table
            data["ds_id"] = ds_id
            utilities.toPostgreSQL(
                data,
                DB_URL,
                schema="data",
            )

            # Create empty spatial table
            spatial = pd.DataFrame()
            spatial[["fid", "ds_id"]] = data[["fid", "ds_id"]]
            utilities.toPostgreSQL(
                spatial,
                DB_URL,
                schema="spatial",
            )
