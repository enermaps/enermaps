#!/usr/bin/env python3
"""
Prepare the ESM dataset and EUDEM for EnerMaps.

Note that the 25-m (EU-DEM) and 2.5-m (ESM) resolution files must be downloaded from Copernicus (requires log-in)
and extracted in the data/21 and data/35 directory.
This script expects that the original zip file from Copernicus is extracted
in multiple zip files, which will be then extracted and tiled.


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
from shapely.geometry import box

N_FILES = {21: 27, 35: 279}
ISRASTER = True
logging.basicConfig(level=logging.INFO)

DB_URL = utilities.DB_URL


def convertZip(directory: str):
    """Convert files downloaded from Copernicus."""
    files_list = glob.glob(os.path.join(directory, "*.zip"))
    if len(files_list) > 0:
        logging.info("Extracting zip files")
        if not os.path.exists(os.path.join(directory, "orig_tiles")):
            os.mkdir(os.path.join(directory, "orig_tiles"))
        for zipfile in files_list:
            extract_dir = os.path.join(
                os.path.dirname(zipfile), pathlib.Path(zipfile).stem
            )
            extracted = utilities.extractZip(zipfile, extract_dir)
            source_file = [x for x in extracted if x.endswith("TIF")][0]

            logging.info(source_file)

            dest_file = os.path.join(
                os.path.dirname(extract_dir),
                "orig_tiles",
                os.path.basename(extract_dir) + ".tif",
            )
            os.system(  # nosec
                "gdal_translate {source_file} {dest_file}  -of GTIFF --config GDAL_PAM_ENABLED NO -co COMPRESS=DEFLATE -co BIGTIFF=YES".format(
                    source_file=source_file, dest_file=dest_file
                )
            )
            shutil.rmtree(extract_dir)
            os.remove(zipfile)
    else:
        logging.info("There are no zip files to extract")


def tiling(directory: str):
    """Tile data from Copernicus."""
    files_list = glob.glob(os.path.join(directory, "orig_tiles", "*.tif"))
    if len(files_list) > 0:
        logging.info("Tiling")
        for file in files_list:
            target_dir = os.path.join(directory, os.path.basename(file))[:-4]
            os.mkdir(target_dir)
            os.system(  # nosec
                "gdal_retile.py -ps 400 400 -targetDir {target_dir} -csv tiles.csv -csvDelim , {source_file} ".format(
                    target_dir=target_dir, source_file=file
                )
            )
        shutil.rmtree(os.path.join(directory, "orig_tiles"))
    else:
        logging.info("There are no files to tile")


def get(directory):
    """Prepare df and gdf with ESM data."""
    files_list = glob.glob(os.path.join(directory, "*", "*.csv"))
    data = []
    for file in files_list:
        logging.info(file)
        tiles = pd.read_csv(file, header=None)
        tiles.columns = ["tilename", "minx", "maxx", "miny", "maxy"]
        tiles["extentBox"] = tiles.apply(
            lambda x: box(x.minx, x.miny, x.maxx, x.maxy), axis=1
        )
        tiles["tilename"] = (
            os.path.basename(os.path.dirname(file)) + "/" + tiles["tilename"]
        )
        data.append(tiles)
    data = pd.concat(data, ignore_index=True)

    enermaps_data = utilities.ENERMAPS_DF
    enermaps_data["fid"] = data["tilename"]
    enermaps_data["variable"] = ""
    enermaps_data["israster"] = ISRASTER

    spatial = gpd.GeoDataFrame(geometry=data["extentBox"], crs="EPSG:3035",)
    spatial["fid"] = data["tilename"]

    return enermaps_data, spatial


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)

    for ds_id in ds_ids:

        directory = "data/{}".format(ds_id)

        if (
            os.path.exists(directory)
            and os.path.isdir(directory)
            and len(os.listdir(directory)) == N_FILES[ds_id]
        ):
            # Dezip
            convertZip(directory)

            # Retile
            tiling(directory)

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

            # Create spatial table
            spatial["ds_id"] = ds_id
            utilities.toPostGIS(
                spatial, DB_URL, schema="spatial",
            )
        else:
            logging.error(
                "The {} directory must exist and contain {} files from Copernicus.".format(
                    directory, N_FILES
                )
            )
