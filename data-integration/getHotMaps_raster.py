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
DS_LIST = {
    31: "https://gitlab.com/gperonato/potential_geothermal_raster/-/raw/naming-correction/",  # to replace when PR will be approved on hotmaps
    43: "https://gitlab.com/hotmaps/heat/heat_tot_curr_density/-/raw/master/",
    45: "https://gitlab.com/hotmaps/gfa_tot_curr_density/-/raw/master/",
}


Force = False  # Force update
logging.basicConfig(level=logging.INFO)

# In Docker
host = "db"
port = 5432
print(host, port)
# Local
# host = "localhost"
# port = 5433


def get(repository: str, dp: frictionless.package.Package, force: bool = False):
    """
    Retrieve (meta)data and check whether an update is necessary.

    Parameters
    ----------
    repository : str
        URL of the Gitlab repository (raw).
    dp : frictionless.package.Package
        Existing dp or None.
    force : bool, optional
        Force update. The default is False.

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
                if [dp["resources"][r]["stats"] != new_dp["resources"][r]["stats"]]:
                    ChangedStats = True
    rasters = pd.DataFrame(rasters)

    if dp != None:
        # check stats
        ChangedVersion = dp["version"] != new_dp["version"]
        if ChangedStats or ChangedVersion:
            logging.info("Data has changed")
        elif force:
            logging.info("Forced update")
        else:
            logging.info(
                "Data has not changed. Use force update if you want to reupload."
            )
            return None

    dp = new_dp

    # Retrieve rasters
    data_enermaps = utilities.prepareRaster(rasters)

    # Move rasters into the data directory
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists(os.path.join("data", str(DS_ID))):
        os.mkdir(os.path.join("data", str(DS_ID)))
    for i, row in data_enermaps.iterrows():
        os.rename(row.FID, os.path.join("data", str(DS_ID), row.FID))

    return data_enermaps, dp


if __name__ == "__main__":
    DS_IDs = DS_LIST.keys()
    if len(sys.argv) > 0:
        parser = argparse.ArgumentParser(description="Import HotMaps raster")
        parser.add_argument("--force", action="store_const", const=True, default=False)
        parser.add_argument(
            "--select_ds_ids", action="extend", nargs="+", type=int, default=[]
        )
        args = parser.parse_args()
        Force = args.force
        if len(args.select_ds_ids) > 0:
            DS_IDs = args.select_ds_ids

    for DS_ID in DS_IDs:
        logging.info("Retrieving Dataset {}".format(DS_ID))
        dp = utilities.getDataPackage(
            DS_ID,
            "postgresql://test:example@{host}:{port}/dataset".format(
                host=host, port=port
            ),
        )

        if (
            utilities.datasetExists(
                DS_ID,
                "postgresql://test:example@{host}:{port}/dataset".format(
                    host=host, port=port
                ),
            )
            and Force == False
        ):
            logging.warning("Dataset already exists. Use force update to replace.")
        else:
            if utilities.datasetExists(
                DS_ID,
                "postgresql://test:example@{host}:{port}/dataset".format(
                    host=host, port=port
                ),
            ):
                utilities.removeDataset(
                    DS_ID,
                    "postgresql://test:example@{host}:{port}/dataset".format(
                        host=host, port=port
                    ),
                )
                logging.info("Removed existing dataset")

            data, dp = get(DS_LIST[DS_ID], dp, Force)

            # Create dataset table
            datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
            metadata = datasets.loc[DS_ID].fillna("").to_dict()
            metadata["datapackage"] = dp
            metadata = json.dumps(metadata)
            dataset = pd.DataFrame([{"ds_id": DS_ID, "metadata": metadata}])
            utilities.toPostgreSQL(
                dataset,
                "postgresql://test:example@{host}:{port}/dataset".format(
                    host=host, port=port
                ),
                schema="datasets",
            )

            # Create data table
            data["ds_id"] = DS_ID
            utilities.toPostgreSQL(
                data,
                "postgresql://test:example@{host}:{port}/dataset".format(
                    host=host, port=port
                ),
                schema="data",
            )

            # Create empty spatial table
            spatial = pd.DataFrame()
            spatial[["FID", "ds_id"]] = data[["FID", "ds_id"]]
            utilities.toPostgreSQL(
                spatial,
                "postgresql://test:example@{host}:{port}/dataset".format(
                    host=host, port=port
                ),
                schema="spatial",
            )
