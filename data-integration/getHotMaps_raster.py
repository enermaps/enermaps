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
import shutil
import sys

import frictionless
import pandas as pd
import utilities

# Constants
logging.basicConfig(level=logging.INFO)
Z = None
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
    isChangedStats = False  # initialize check

    # Prepare df containing paths to rasters
    rasters = []
    for resource_idx in range(len(new_dp["resources"])):
        if "temporal" in new_dp["resources"][resource_idx]:
            start_at = pd.to_datetime(
                new_dp["resources"][resource_idx]["temporal"]["start"]
            )
        else:
            start_at = None

        if "unit" in new_dp["resources"][resource_idx]:
            unit = new_dp["resources"][resource_idx]["unit"]
        else:
            unit = None

        if new_dp["resources"][resource_idx]["format"] == "tif":
            logging.info(new_dp["resources"][resource_idx]["path"])
            utilities.download_url(
                repository + new_dp["resources"][resource_idx]["path"],
                os.path.basename(new_dp["resources"][resource_idx]["path"]),
            )
            raster = {
                "value": os.path.basename(new_dp["resources"][resource_idx]["path"]),
                "start_at": start_at,
                "z": Z,
                "unit": unit,
                "dt": DT,
            }
            rasters.append(raster)
            # check statistics for each resource
            if dp is not None and "stats" in new_dp["resources"][resource_idx]:
                if (
                    dp["resources"][resource_idx]["stats"]
                    != new_dp["resources"][resource_idx]["stats"]
                ):
                    isChangedStats = True
    rasters = pd.DataFrame(rasters)

    if dp is not None:  # Existing dataset
        # check stats
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

    # Move rasters into the data directory
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists(os.path.join("data", str(ds_id))):
        os.mkdir(os.path.join("data", str(ds_id)))
    for i, row in data_enermaps.iterrows():
        shutil.move(row.fid, os.path.join("data", str(ds_id), row.fid))

    return data_enermaps, new_dp


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

            # Create empty spatial table
            spatial = pd.DataFrame()
            spatial[["fid", "ds_id"]] = data[["fid", "ds_id"]]
            utilities.toPostgreSQL(
                spatial, DB_URL, schema="spatial",
            )
