#!/usr/bin/env python3
"""
Prepare the SolarAtlas dataset for EnerMaps.

Note that the annual monthly files must be downloaded from the SolarAtlas website
and extracted in the data/24 directory
Download the file from here: https://globalsolaratlas.info/download/europe-and-central-asia
Gis data - LTAym_YearlyMonthlyTotals (GeoTIFF)
Data format: GEOTIFF
File size : 3.44 GB
The data/24 directory should contain only the "monthly" directory from the download files.
The original monthly files will be then translated and tiled.

@author: giuseppeperonato
"""

import glob
import json
import logging
import os
import shutil
import sys

import geopandas as gpd
import pandas as pd
import utilities
from shapely.geometry import box

ISRASTER = True
UNIT = "kWh/kWp"
VARIABLE = "Longterm monthly average of potential photovoltaic electricity production"
SRS = "EPSG:3035"
DT = 720
logging.basicConfig(level=logging.INFO)

DB_URL = utilities.DB_URL


def convertFiles(directory: str):
    """Convert files downloaded from Solar Atlas."""
    files_list = glob.glob(os.path.join(directory, "*.tif"))
    if len(files_list) > 0:
        logging.info("Converting files")
        if not os.path.exists(
            os.path.join(os.path.dirname(directory), "converted_files")
        ):
            os.mkdir(os.path.join(os.path.dirname(directory), "converted_files"))
        for source_file in files_list:

            logging.info(source_file)

            dest_file = os.path.join(
                os.path.dirname(directory),
                "converted_files",
                os.path.basename(source_file),
            )
            os.system(  # nosec
                "gdalwarp {source_file} {dest_file} -of GTIFF -s_srs EPSG:4326 -t_srs {outputSRS}  --config GDAL_PAM_ENABLED NO -co COMPRESS=DEFLATE -co BIGTIFF=YES".format(
                    source_file=source_file, dest_file=dest_file, outputSRS=SRS
                )
            )
    else:
        logging.info("There are no tif files to extract")


def tiling(directory: str):
    """Tile data from Solar Atlas."""
    files_list = glob.glob(os.path.join(directory, "converted_files", "*.tif"))
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
        shutil.rmtree(os.path.join(directory, "converted_files"))
    else:
        logging.info("There are no files to tile")


def get(directory):
    """Prepare df and gdf with solar atlas tiled data."""
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
        tiles["start_at"] = pd.to_datetime(
            "2099-" + os.path.dirname(file).split("_")[1], format="%Y-%m"
        )
        data.append(tiles)
    data = pd.concat(data, ignore_index=True)

    enermaps_data = utilities.ENERMAPS_DF
    enermaps_data["fid"] = data["tilename"]
    enermaps_data["start_at"] = data["start_at"]
    enermaps_data["variable"] = VARIABLE
    enermaps_data["unit"] = UNIT
    enermaps_data["israster"] = ISRASTER
    enermaps_data["dt"] = DT

    spatial = gpd.GeoDataFrame(geometry=data["extentBox"], crs="EPSG:3035",)
    spatial["fid"] = data["tilename"]

    return enermaps_data, spatial


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)

    for ds_id in ds_ids:

        directory = "data/{}".format(ds_id)

        if os.path.exists(directory) and os.path.isdir(directory):
            # Convert
            convertFiles(os.path.join(directory, "monthly"))

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
                "The {} directory must exist and contain files from Solar Atlas.".format(
                    directory,
                )
            )
