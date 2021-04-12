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

import frictionless
import pandas as pd

import utilities

# Constants
logging.basicConfig(level=logging.INFO)

# In Docker
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")


def get(repository: str, dp: frictionless.package.Package, isForced: bool = False):
    """
    Retrieve (meta)data and check whether an update is necessary.

    Parameters
    ----------
    repository : str
        URL of the Gitlab repository (raw).
    dp : frictionless.package.Package
        Existing dp or None.
    isForced : bool, optional
        isForced update. The default is False.

    Returns
    -------
    data_enermaps : DataFrame
        df in EnerMaps format.
    dp : frictionless.package.Package
        Datapackage corresponding to the data.

    """
    new_dp = frictionless.Package(repository + "datapackage.json")
    ChangedStats = False  # initialize check

    # Prepare df containing paths to rasters
    rasters = []
    for r in range(len(new_dp["resources"])):
        if "temporal" in new_dp["resources"][r]:
            time = pd.to_datetime(new_dp["resources"][r]["temporal"]["start"])
        else:
            time = None

        if "unit" in new_dp["resources"][r]:
            unit = new_dp["resources"][r]["unit"]
        else:
            unit = None

        if new_dp["resources"][r]["format"] == "tif":
            logging.info(new_dp["resources"][r]["path"])
            utilities.download_url(
                repository + new_dp["resources"][r]["path"],
                os.path.basename(new_dp["resources"][r]["path"]),
            )
            raster = {
                "value": os.path.basename(new_dp["resources"][r]["path"]),
                "time": time,
                "z": None,
                "unit": unit,
                "dt": 8760,
            }
            rasters.append(raster)
            # check statistics for each resource
            if dp != None and "stats" in new_dp["resources"][r]:
                if dp["resources"][r]["stats"] != new_dp["resources"][r]["stats"]:
                    ChangedStats = True
    rasters = pd.DataFrame(rasters)

    if dp != None:
        # check stats
        ChangedVersion = dp["version"] != new_dp["version"]
        if ChangedStats or ChangedVersion:
            logging.info("Data has changed")
        elif isForced:
            logging.info("Forced update")
        else:
            logging.info("Data has not changed. Use --Force if you want to reupload.")
            return None

    dp = new_dp

    # Retrieve rasters
    data_enermaps = utilities.prepareRaster(rasters, delete_orig=True)

    # Move rasters into the data directory
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists(os.path.join("data", str(ds_id))):
        os.mkdir(os.path.join("data", str(ds_id)))
    for i, row in data_enermaps.iterrows():
        os.rename(row.FID, os.path.join("data", str(ds_id), row.FID))

    return data_enermaps, dp


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

        if (
            utilities.datasetExists(
                ds_id,
                "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                    DB_HOST=DB_HOST,
                    DB_PORT=DB_PORT,
                    DB_USER=DB_USER,
                    DB_PASSWORD=DB_PASSWORD,
                    DB_DB=DB_DB,
                ),
            )
            and isForced == False
        ):
            logging.warning("Dataset already exists. Use isForced update to replace.")
        else:
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
                logging.info("Removed existing dataset")

            data, dp = get(datasets.loc[ds_id, "di_URL"], dp, isForced)

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

            # Create empty spatial table
            spatial = pd.DataFrame()
            spatial[["FID", "ds_id"]] = data[["FID", "ds_id"]]
            utilities.toPostgreSQL(
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
