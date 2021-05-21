#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare the ESM dataset for EnerMaps.

Note that the 2.5-m resolution files must be downloaded from Copernicus (requires log-in)
and extracted in the data/21 directory.
This script expects that the original zip file from Copernicus is extracted
in multiple zip files, which will be then converted in GeoTIFF.
Created on Fri May 21 09:51:41 2021

@author: giuseppeperonato
"""

import glob
import json
import logging
import os
import pathlib
import shutil
import sys

import geopandas as gpd
import pandas as pd
import utilities
from osgeo import gdal, osr
from pyproj import CRS
from shapely.geometry import box

N_FILES = 279
ISRASTER = True
logging.basicConfig(level=logging.INFO)

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


def getExtentBox(ds):
    """Return shapely box of corner coordinates from a gdal Dataset."""
    xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
    width, height = ds.RasterXSize, ds.RasterYSize
    xmax = xmin + width * xpixel
    ymin = ymax + height * ypixel

    return box(xmin, ymin, xmax, ymax)


def convertZip(directory: str):
    """Convert files downloaded from Copernicus."""
    files_list = glob.glob(os.path.join(directory, "*.zip"))
    if len(files_list) > 0:
        logging.info("Extracting zip files")
        for zipfile in files_list:
            try:
                assert len(files_list) == N_FILES
            except AssertionError:
                logging.error(
                    "You should manually upload the files downloaded from Copernicus."
                )
            extract_dir = os.path.join(
                os.path.dirname(zipfile), pathlib.Path(zipfile).stem
            )
            extracted = utilities.extractZip(zipfile, extract_dir)
            source_file = [x for x in extracted if x.endswith("TIF")][0]

            logging.info(source_file)

            dest_file = extract_dir + ".tif"
            os.system(
                "gdal_translate {source_file} {dest_file}  -of GTIFF --config GDAL_PAM_ENABLED NO -co COMPRESS=DEFLATE -co BIGTIFF=YES".format(
                    source_file=source_file, dest_file=dest_file
                )
            )
            shutil.rmtree(extract_dir)
            shutil.rmtree(zipfile)
    else:
        logging.info("There are no zip files to extract")


def get(directory):
    """Prepare df and gdf with ESM data."""
    files_list = glob.glob(os.path.join(directory, "*.tif"))
    fids = []
    extents = []
    for file in files_list:
        try:
            assert len(files_list) == N_FILES
        except AssertionError:
            logging.error(
                "You should manually upload the files downloaded from Copernicus."
            )
        logging.info(file)
        src_ds = gdal.Open(file)
        prj = src_ds.GetProjection()
        srs = osr.SpatialReference(wkt=prj)
        source_crs = CRS.from_epsg(srs.GetAttrValue("authority", 1))

        try:
            assert source_crs.to_string() == "EPSG:3035"
        except AssertionError:
            logging.error("Input files must be in EPSG:3035")

        extentBox = getExtentBox(src_ds)
        fids.append(os.path.basename(file))
        extents.append(extentBox)

    enermaps_data = pd.DataFrame(
        columns=[
            "start_at",
            "fields",
            "variable",
            "value",
            "ds_id",
            "fid",
            "dt",
            "z",
            "israster",
            "unit",
        ]
    )
    enermaps_data["fid"] = fids

    spatial = gpd.GeoDataFrame(geometry=extents, crs="EPSG:3035",)
    spatial["fid"] = fids

    return enermaps_data, spatial


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

    directory = "data/{}".format(ds_id)

    try:
        assert os.path.exists(directory)
        assert os.path.isdirectory(directory)
        assert len(os.listdir(directory)) > 0
    except AssertionError:
        logging.error(
            "The {} directory must exist and contain {} files from Copernicus.".format(
                directory, N_FILES
            )
        )

    convertZip(directory)
    data, spatial = get(directory)

    # Remove existing dataset
    if utilities.datasetExists(ds_id, DB_URL) and not isForced:
        raise FileExistsError("Use --force to replace the existing dataset.")
    elif utilities.datasetExists(ds_id, DB_URL) and isForced:
        utilities.removeDataset(ds_id, DB_URL)
        logging.info("Removed existing dataset")
    else:
        pass

    # Create dataset table
    metadata = datasets.loc[ds_id].fillna("").to_dict()
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
    spatial["ds_id"] = ds_id
    utilities.toPostgreSQL(
        spatial, DB_URL, schema="spatial",
    )
