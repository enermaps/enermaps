#!/usr/bin/env python3
"""
Pipeline for PANGAEA data, with custom NETCDF reading.
This script allows for data updates.

@author: giuseppeperonato
"""

import json
import logging
import os
import shutil
import sys

import frictionless
import numpy as np
import pandas as pd
import requests
import utilities
import xarray
from pyproj import CRS

# Constants
logging.basicConfig(level=logging.INFO)
Z = None
DT = 720
SEL = "MON"
EPSG = 4326  # source

DB_URL = utilities.DB_URL


def prepareNETCDF(
    df: pd.DataFrame, crs: CRS = CRS.from_epsg(3035), delete_orig: bool = False,
):
    """
    Convert  NetCDF into EnerMaps rasters (single band, GeoTiff, EPSG:3035).
    Adapted to multi-dimensional NetCDF files as the ones from PANGAEA.

    Parameters
    ----------
    df : DataFrame.
        Results of API extraction.
    crs : pyproj.crs.CRS.
       coordinate reference system.
    delete_orig : bool, optional.
        Set to True to delete original downloaded file (e.g. NetCDF).

    Returns
    -------
    df : DataFrame
        Results with schema for EnerMaps data table

    """
    dicts = []
    for i, row in df.iterrows():
        filename_orig = row["value"]
        logging.info(filename_orig)
        xds = xarray.open_dataset(filename_orig)
        if "crs" not in df.columns:
            raise ValueError("Missing crs")
        if "variable" not in df.columns:
            raise ValueError("Missing variable")

        xds.rio.write_crs(row["crs"].to_string(), inplace=True)

        variable = row.variable
        dims = list(xds[variable].dims)

        if "lat" in dims:
            dims.remove("lat")
        if "lon" in dims:
            dims.remove("lon")

        def np_encoder(object):
            """Source: https://stackoverflow.com/a/65151218."""
            if isinstance(object, np.generic):
                return object.item()

        def prepareFile(tmp_filename, dest_filename, my_dict, filename_orig):
            """Export raster."""
            if not os.path.exists(tmp_filename):
                reprojected.rio.to_raster(tmp_filename)
            dicts.append(my_dict)

            # Compress
            os.system(  # nosec
                "gdal_translate {filename} {dest_filename} -of GTIFF --config GDAL_PAM_ENABLED NO -co COMPRESS=DEFLATE -co BIGTIFF=YES".format(
                    filename=tmp_filename, dest_filename=dest_filename
                )
            )

            os.remove(tmp_filename)

            return dicts

        if len(dims) == 2:
            for d0 in range(xds[variable][dims[0]].shape[0]):
                for d1 in range(xds[variable][dims[1]].shape[0]):
                    my_dict = {}
                    dest_filename = "{}_{}_{}.tif".format(
                        filename_orig.split(".")[0], d0, d1
                    )
                    tmp_filename = "{}_{}_{}_tmp.tif".format(
                        filename_orig.split(".")[0], d0, d1
                    )

                    my_dict["fid"] = os.path.basename(dest_filename)
                    my_dict["variable"] = xds[variable][d0][d1].attrs["long_name"]
                    my_dict["unit"] = xds[variable][d0].attrs.get("units")

                    # Add extra fields
                    my_dict["fields"] = {
                        **xds.attrs,  # at the dataset level
                        **xds[variable][d0][d1].attrs,
                    }  # at the dimension level
                    for dim in dims:
                        if dim != "time":  # add information about extra dimensions
                            my_dict["fields"][dim] = str(
                                xds[variable][d0][d1][dim].values
                            )

                    my_dict["fields"] = json.dumps(
                        my_dict["fields"], default=np_encoder
                    )

                    my_dict["israster"] = True

                    my_dict["start_at"] = pd.to_datetime(
                        xds[variable][d0][d1].time.values
                    )
                    date_future = my_dict["start_at"] + pd.DateOffset(months=1)
                    my_dict["dt"] = (
                        date_future - my_dict["start_at"]
                    ).total_seconds() / 3600

                    # reproj
                    reprojected = xds[variable][d0][d1].rio.reproject(crs.to_string())

                    dicts = prepareFile(
                        tmp_filename, dest_filename, my_dict, filename_orig
                    )

        elif len(dims) == 1:
            for d0 in range(xds[variable][dims[0]].shape[0]):
                my_dict = {}
                dest_filename = "{}_{}.tif".format(filename_orig.split(".")[0], d0)
                tmp_filename = "{}_{}_tmp.tif".format(filename_orig.split(".")[0], d0)

                my_dict["fid"] = os.path.basename(dest_filename)
                my_dict["variable"] = xds[variable][d0].attrs["long_name"]
                my_dict["unit"] = xds[variable][d0].attrs.get("units")

                # Add extra fields
                my_dict["fields"] = {
                    **xds.attrs,  # at the dataset level
                    **xds[variable][d0].attrs,
                }  # at the dimension level
                my_dict["fields"] = json.dumps(my_dict["fields"], default=np_encoder)

                my_dict["israster"] = True

                my_dict["start_at"] = pd.to_datetime(xds[variable][d0].time.values)
                date_future = my_dict["start_at"] + pd.DateOffset(months=1)
                my_dict["dt"] = (
                    date_future - my_dict["start_at"]
                ).total_seconds() / 3600

                # Reproject
                if xds[variable][d0].dtype == "<m8[ns]":
                    # otherwise an error is thrown
                    reprojected = (
                        xds[variable][d0]
                        .astype(np.float32)
                        .rio.reproject(crs.to_string())
                    )
                else:
                    reprojected = xds[variable][d0].rio.reproject(crs.to_string())

                dicts = prepareFile(tmp_filename, dest_filename, my_dict, filename_orig)
        else:
            raise ValueError("Too many dimensions")

    if delete_orig:
        os.remove(filename_orig)

    data = pd.DataFrame(
        dicts,
        columns=[
            "start_at",
            "fields",
            "variable",
            "value",
            "ds_id",
            "fid",
            "dt",
            "z",
            "unit",
            "israster",
        ],
    )

    return data


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
    """
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    for resource_idx, resource in enumerate(dp["resources"]):
        file_list = resource["path"]
        r = requests.get(file_list, stream=True)
        lines = [line for line in r.iter_lines()]
        skiprows = [ind for ind, i in enumerate(lines) if i.startswith(b"*/")][0]
        files = pd.read_csv(file_list, skiprows=skiprows + 1, delimiter="\t")
        files = files.loc[files["File name"].str.contains(SEL), :]

        # Prepare df containing paths to rasters
        rasters = []
        for r, row in files.iterrows():
            if not os.path.exists(os.path.join("tmp", row["File name"])):
                logging.info("Downloading {}".format(row["File name"]))
                utilities.download_url(
                    row["URL file"], os.path.join("tmp", row["File name"])
                )
            raster = {
                "value": os.path.join("tmp", row["File name"]),
                "start_at": pd.to_datetime(row["File name"].split("_")[6]),
                "z": None,
                "unit": None,
                "dt": DT,
                "crs": CRS.from_epsg(EPSG),
                "variable": row["File name"].split("_")[0],
            }
            rasters.append(raster)
    rasters = pd.DataFrame(rasters)
    data_enermaps = prepareNETCDF(rasters, delete_orig=True)

    return data_enermaps


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
            if (
                resource["encodingFormat"] == "CSV"
                or resource["encodingFormat"] == "text/tab-separated-values"
            ):
                file = resource["contentUrl"]
    datePublished = ld["datePublished"]

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")
    new_dp = frictionless.describe_package(file, stats=True,)  # Add stats
    # Add date
    new_dp["datePublished"] = datePublished

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        isChangedStats = dp["resources"][0]["stats"] != new_dp["resources"][0]["stats"]
        isChangedDate = dp["datePublished"] != new_dp["datePublished"]

        if (
            isChangedStats or isChangedDate
        ):  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            if utilities.isDFvalid(dp, new_dp):
                enermaps_data = prepare(new_dp)
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            if utilities.isDFvalid(dp, new_dp):
                enermaps_data = prepare(new_dp)
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None, None
    else:  # New dataset
        dp = new_dp  # this is just for the sake of the schema control
        if utilities.isDFvalid(dp, new_dp):
            enermaps_data = prepare(new_dp)

    return enermaps_data, new_dp


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)

    for ds_id in ds_ids:
        logging.info("Retrieving Dataset {}".format(ds_id))
        dp = utilities.getDataPackage(ds_id, DB_URL,)

        data, dp = get(datasets.loc[ds_id, "di_URL"], dp, isForced)

        # Move rasters into the data directory
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists(os.path.join("data", str(ds_id))):
            os.mkdir(os.path.join("data", str(ds_id)))
        for i, row in data.iterrows():
            try:
                shutil.move(
                    os.path.join("tmp", row.fid),
                    os.path.join("data", str(ds_id), row.fid),
                )
            except FileNotFoundError:
                logging.error("File not found; {}".format(row.fid))

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
