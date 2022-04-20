#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute breaks for the legends of each layer, then upload legends on the server

@author: manueldalcastagne
"""

import json
import math
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import requests
import sqlalchemy as sqla
from scipy.stats import qmc


# retrieve colors in RGB format from the color table
def get_colors(clrpath: Path) -> Dict[str, List[Tuple[float, float, float]]]:
    SEP = ","
    clrs = {}
    with open(clrpath, mode="r") as clrfile:
        # skip the header
        _ = next(clrfile).split(SEP)
        for line in clrfile:
            key, *vals = line.split(SEP)
            clrs[key] = [
                tuple([int(v[2:]) / 255.0 for v in rgb.split()]) for rgb in vals
            ]
    return clrs


# format the input string in order to be a valid filename
def format_filename(input_str: str) -> str:
    valid_fname = input_str.replace(" ", "")
    valid_fname = re.sub(r"[^\w\s-]", "", valid_fname.lower())
    valid_fname = re.sub(r"[-\s]+", "-", valid_fname).strip("-_")
    return valid_fname


# ------------------------------
# settings and setup
# ------------------------------

# folders and files settings
SRCDIR = Path(__file__).parent
DATADIR = SRCDIR.parent / "data"
BREAKSDIR = DATADIR / "breaks"
CLRTABLE = "color-tables.csv"
LAYERTABLE = "layers.csv"

# breaks and layers settings
ROW_LIMIT = 100000  # limit the data requests to the server
MAX_LENGTH = 1000  # max height or width of a raster to be allowed to read the whole file in memory at once
MAX_SIZE = 100000  # max size to sample a layer - to compute percentiles for legends
SAMPLE_SIZE = (
    512  # size of the sample of a single raster of the layer - use a multiple of 2
)
percentiles_list = [20, 40, 60, 80]  # percentiles used to compute legend breaks
EXCLUDED = [
    467,
    474,
]  # layers to exclude - custom legend has been set during data-integration
API_KEY = os.environ.get(
    "API_KEY"
)  # private key required to upload the legends on the server

# database settings
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")
db_connection_url = (
    "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_DB=DB_DB,
    )
)

if not os.path.exists(BREAKSDIR):
    os.mkdir(BREAKSDIR)
if not os.path.exists(LAYERTABLE):
    raise FileNotFoundError(
        "Layer list not found. Please check your .env file and the content of local"
        " folders."
    )
if not os.path.exists(CLRTABLE):
    raise FileNotFoundError(
        "Color list not found. Please check your .env file and the content of local"
        " folders."
    )

# read colors and layer names
colors_dict = get_colors(CLRTABLE)
layers = pd.read_csv(LAYERTABLE)
layers["uploaded"] = 0

# ------------------------------
# computing breaks
# ------------------------------

for i, row in layers.iterrows():

    # get layer's data, colors and type (raster or not)
    ds_id = row["ds_id"]
    variable = row["variable"]
    valid_fname = format_filename(variable)
    isRaster = row["israster"]
    data_class = row["class_of_data"]
    clrs = colors_dict[data_class]

    # create and execute query to retrieve vectors/rasters of the layer
    parameters = {"data.ds_id": str(ds_id)}
    if variable:
        parameters["variable"] = "''{}''".format(variable)
    query = "SELECT * from enermaps_query_table('{}', {}, 0)"
    query = query.format(json.dumps(parameters), ROW_LIMIT)
    con = sqla.create_engine(db_connection_url)
    gdf = gpd.GeoDataFrame.from_postgis(query, con, geom_col="geometry")

    if len(gdf) > 0:

        # access and process data of each layer
        total_sample_data = np.empty(0)
        layer_path = BREAKSDIR / "{}_{}.txt".format(ds_id, valid_fname)

        print(
            "\ndataset {} - {}: {} data vectors/rasters found\n".format(
                ds_id, variable, len(gdf)
            )
        )

        # only raster data needs more advanced processing
        if isRaster:

            print(
                'Computing legend breaks - dataset {}, layer "{}"\n'.format(
                    ds_id, variable
                )
            )
            breaks_min = float("inf")
            breaks_max = float("-inf")

            # path to the directory containing raster data of a dataset on the server
            data_path = DATADIR / "{}".format(ds_id)

            # for each raster of a layer
            for i, record in gdf.iterrows():
                fid = gdf.iloc[i]["fid"]
                fid_path = data_path / "{}".format(fid)

                print("Processing raster file {}".format(fid))
                with rasterio.open(fid_path) as ds:

                    if ds.count > 1:
                        raise ValueError(
                            "The raster has multiple bands", ds_id, variable, fid
                        )

                    # read block by block (smaller memory footprint, but slower - more IO operations)
                    if ds.meta["width"] > MAX_LENGTH or ds.meta["height"] > MAX_LENGTH:
                        blocks_data = []
                        # filter out nodata values, flatten the output to 1d array and concatenate lists
                        for _, window_read in ds.block_windows(1):
                            block = ds.read(window=window_read)
                            if type(ds.nodata) == float:
                                block = block.astype(float)
                            block[block == ds.nodata] = np.nan
                            block = block[~np.isnan(block)]
                            blocks_data.extend(block)

                    # read the whole raster (larger memory footprint, but faster - less IO operations)
                    else:
                        # filter out nodata values and flatten the output to 1d array
                        blocks_data = ds.read(1)
                        if type(ds.nodata) == float:
                            blocks_data = blocks_data.astype(float)
                        blocks_data[blocks_data == ds.nodata] = np.nan
                        blocks_data = blocks_data[~np.isnan(blocks_data)]

                    # adapt the sample space to the size of the raster, then sample using scrambled Sobol sequences (use multiples of 2)
                    if len(total_sample_data) < MAX_SIZE:
                        l_bounds = [0]
                        u_bounds = [len(blocks_data)]
                        sample_data = np.empty(0)
                        m_exp = np.ceil(math.log(SAMPLE_SIZE, 2)).astype(int)
                        sampler = qmc.Sobol(d=1, scramble=True, seed=1)
                        sample = sampler.random_base2(m_exp)
                        sample = qmc.scale(sample, l_bounds, u_bounds)
                        sample = np.rint(sample).astype(int)
                        for sample_coords in sample:
                            index = sample_coords[0]
                            val = blocks_data[index]
                            sample_data = np.append(sample_data, val)
                        total_sample_data = np.append(total_sample_data, sample_data)

                    # compute min and max of the whole layer
                    breaks_min = min(breaks_min, np.min(blocks_data))
                    breaks_max = max(breaks_max, np.max(blocks_data))

            # computing breaks, considering all rasters
            breaks = np.percentile(total_sample_data, percentiles_list)

        else:
            print(
                'Computing legend breaks - dataset {}, layer "{}"\n'.format(
                    ds_id, variable
                )
            )
            vector = gdf
            vector["variable"] = vector["variables"].apply(
                lambda x: list(x.values())[0]
            )
            data = np.array(vector["variable"])

            breaks = np.percentile(data, percentiles_list)
            breaks_min = np.min(data)
            breaks_max = np.max(data)

        # round and export unique breaks
        breaks_output = np.append(breaks_min, breaks)
        breaks_output = np.append(breaks_output, breaks_max)
        breaks_output = np.unique(np.around(breaks_output, decimals=2))

        if np.sum(breaks_output) == 0:
            raise ValueError("All the breaks of the layer are 0", ds_id, variable, fid)
        if len(breaks_output) < 2:
            raise ValueError("The breaks are less than 2")

        with open(layer_path, "w") as f:
            np.savetxt(f, breaks_output)

    else:
        print('No data found for dataset\'s {} layer "{}"'.format(ds_id, variable))

# ------------------------------
# loading legends
# ------------------------------

for i, row in layers.iterrows():

    if i not in EXCLUDED:
        ds_id = row["ds_id"]
        variable = row["variable"]
        valid_fname = format_filename(variable)
        data_class = row["class_of_data"]
        clrs = colors_dict[data_class]
        layer_path = BREAKSDIR / "{}_{}.txt".format(ds_id, valid_fname)

        if os.path.exists(layer_path):
            print("Uploading legend - dataset {} - {}".format(ds_id, variable))
            legend = {"name": variable, "type": "custom", "symbology": []}
            breaks = np.loadtxt(layer_path)

            # prepare the legend without considering the last break
            for color_index in range(len(breaks) - 1):
                red = int(clrs[color_index][0] * 255)
                green = int(clrs[color_index][1] * 255)
                blue = int(clrs[color_index][2] * 255)
                legend["symbology"].append(
                    {
                        "red": red,
                        "green": green,
                        "blue": blue,
                        "opacity": 1.0,
                        "value": breaks[color_index],
                        "label": "≥ "
                        + str(round(breaks[color_index], 2))
                        + " "
                        + str(row["unit"]),
                    }
                )

            # send the legend
            r = requests.post(
                "https://lab.idiap.ch/enermaps/api/db/rpc/enermaps_set_legend",
                headers={"Authorization": "Bearer {}".format(API_KEY)},
                json={
                    # SELECT A LAYER
                    "parameters": {
                        "data.ds_id": str(ds_id),
                        "variable": "'{}'".format(variable),
                    },
                    # SET A LEGEND
                    "legend": legend,
                },
            )

            # check returned code (https://github.com/enermaps/doc/blob/main/legends.md)
            if r.status_code == 200:
                print("Successful upload")
            else:
                raise ValueError(
                    "Something went wrong during the upload (ERROR CODE {}).".format(
                        r.status_code
                    )
                )

    else:
        print("{} legend not found".format(layer_path))
