#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 08:37:08 2021

@author: giuseppeperonato
"""

import argparse
import json
import logging
import os
import shutil
import sys
import zipfile

import frictionless
import pandas as pd
import requests
import utilities
from pyproj import CRS

# Constants
logging.basicConfig(level=logging.INFO)
Z = None
UNIT = "W/m2"
DT = 720
RASTER_META = {"epsg": "4326"}

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

SUBDATASETS = [
    {
        "path": "http://re.jrc.ec.europa.eu/pvg_download/cmsafdata/gh_0_month_cmsaf.zip",
        "unit": UNIT,
        "raster": RASTER_META,
    },
    {
        "path": "http://re.jrc.ec.europa.eu/pvg_download/cmsafdata/gh_opt_month_cmsaf.zip",
        "unit": UNIT,
        "raster": RASTER_META,
    },
    {
        "path": "http://re.jrc.ec.europa.eu/pvg_download/cmsafdata/gh_2a_month_cmsaf.zip",
        "unit": UNIT,
        "raster": RASTER_META,
    },
]


def compileDP(subdatasets: dict = SUBDATASETS):
    """
    Compile a DataPackage of raster files using HotMaps schema.

    Parameters
    ----------
    subdatasets : dict, optional
        List of dicts containg the resource fields. The default is SUBDATASETS.

    Returns
    -------
    frictionless.package.Package
        HotMaps dp for raster resources.

    """
    dp = {"profile": "raster-data-resource", "version": None, "resources": []}
    for resource in subdatasets:
        h = requests.head(resource["path"], allow_redirects=True)
        resource.update(
            {
                "stats": {"bytes": h.headers["Content-Length"]},
                "format": h.headers["Content-Type"],
                "Date": h.headers["Date"],
            }
        )
        dp["resources"].append(resource)
    return frictionless.Package(dp)


def get(dp: frictionless.package.Package, isForced: bool = False):
    """
    Retrieve (meta)data and check whether an update is necessary.

    Parameters
    ----------
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
    new_dp = compileDP()
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

        if new_dp["resources"][resource_idx]["format"] in ["application/zip", "tif"]:
            logging.info(new_dp["resources"][resource_idx]["path"])

            utilities.download_url(
                new_dp["resources"][resource_idx]["path"],
                os.path.basename(new_dp["resources"][resource_idx]["path"]),
            )

            if zipfile.is_zipfile(
                os.path.basename(new_dp["resources"][resource_idx]["path"])
            ):
                extracted = utilities.extractZip(
                    os.path.basename(new_dp["resources"][resource_idx]["path"]), "temp"
                )
            else:
                extracted = os.path.basename(new_dp["resources"][resource_idx]["path"])

            for path in extracted:
                raster = {
                    "value": path,
                    "start_at": start_at,
                    "z": Z,
                    "unit": unit,
                    "dt": DT,
                }

                if new_dp["resources"][resource_idx].get("raster") is not None:
                    raster["crs"] = CRS.from_epsg(
                        new_dp["resources"][resource_idx]["raster"].get("epsg")
                    )

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
    variables = {
        "0": "Monthly average global irradiance on a horizontal surface (W/m2), period 2005-2015",
        "opt": "Monthly average global irradiance on an optimally inclined surface (W/m2), period 2005-2015",
        "2a": "Monthly average global irradiance on a two-axis sun-tracking surface (W/m2), period 2005-2015",
    }
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for i, row in data.iterrows():
        filename = os.path.basename(row["fid"])
        chunks = filename.split("_")
        m = chunks[2]
        var = chunks[1]
        data.loc[i, "start_at"] = pd.to_datetime(
            "2099{}01".format(m), format="%Y%m%d", errors="ignore"
        )
        data.loc[i, "variable"] = variables[var]
        data.loc[i, "dt"] = days_per_month[int(m) - 1] * 24
    return data


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_ids = datasets[datasets["di_script"] == os.path.basename(sys.argv[0])].index
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Import PVGIS raster")
        parser.add_argument("--force", action="store_const", const=True, default=False)
        parser.add_argument(
            "--select_ds_ids", action="extend", nargs="+", type=int, default=[]
        )
        args = parser.parse_args()
        isForced = args.force
        if len(args.select_ds_ids) > 0:
            ds_ids = args.select_ds_ids
    else:
        isForced = True

    for ds_id in ds_ids:
        logging.info("Retrieving Dataset {}".format(ds_id))
        dp = utilities.getDataPackage(ds_id, DB_URL)

        data, dp = get(dp, isForced)

        try:
            data = postProcess(data)
        except NameError:
            pass
        else:
            logging.error("Error in postprocessing.")

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
