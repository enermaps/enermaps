import json
import logging
import os
import shutil
import subprocess  # nosec
import uuid
from time import sleep, time

import geopandas as gpd
import jenkspy
import numpy as np
import pandas as pd
import rasterio
import rasterio.merge as merge
import requests
import urllib3
from BaseCM.cm_output import validate
from matplotlib import cm
from rasterio.mask import mask
from shapely import wkt
from shapely.geometry import Polygon, shape
from shapely.ops import cascaded_union
from tensorflow.keras.backend import clear_session
from tensorflow.keras.models import load_model

# REST API for HDD
POSTGREST_URL = os.environ.get("DATASETS_SERVER_URL", "")
API_KEY = os.environ.get("DATASETS_SERVER_API_KEY", "").replace('"', "")
POSTGREST_ENDPOINT = "rpc/enermaps_query_table"
HEADERS = {"Authorization": "Bearer {}".format(API_KEY)}

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

ESM_dict = {
    1: 1,  # water
    2: 2,  # railways
    10: 3,  # NBU Area - Open Space
    20: 4,  # NBU Area - Green ndvix
    30: 5,  # BU Area - Open Space
    40: 6,  # BU Area - Green ndvix
    41: 7,  # BU Area - Green Urban Atlas
    50: 0,  # BU Area - Built-up
}

MODELS = {
    500: "9216fdce-9855-11eb-b3f9-3e22fb3fc3ab",
    300: "2dcaa71c-9837-11eb-b3f9-3e22fb3fc3ab",
}
PIXEL_SIZE = 2.5
HDD_MODEL = {"slope": -0.0002855045732455094, "intercept": 1.8116549365250931}
MAX_AREA = 2e8  # prevent requests on selection areas larger than 200 km2


def createLegend(
    preds: np.array, name: str = "Heating density", unit: str = "MWh", nb_class: int = 5
) -> dict:
    """Prepare a legend dict in HotMaps format"""
    nb_class = min([nb_class, preds[~np.isnan(preds)].shape[0] - 1])
    if nb_class > 2:
        color_scale = cm.get_cmap("plasma", nb_class).colors
        color_scale[:, :-1] *= 255

        breaks = jenkspy.jenks_breaks(preds[~np.isnan(preds)], nb_class=nb_class)

        legend = {"name": name, "type": "custom", "symbology": []}
        for i in range(len(breaks) - 1):
            legend["symbology"].append(
                {
                    "red": float(color_scale[i, 0]),
                    "green": float(color_scale[i, 1]),
                    "blue": float(color_scale[i, 2]),
                    "opacity": float(color_scale[i, 3]),
                    "value": float(breaks[i]),
                    "label": "≥ {} {}".format(int(round(breaks[i], 0)), unit),
                }
            )
    else:
        legend = {}
        print("No legend was created.", flush=True)
    return legend


def replace_with_dict(array: np.array, dic: dict = ESM_dict):
    """Replace numpy values with dict (source: https://stackoverflow.com/a/47171600)."""

    # Extract out keys and values
    keys = np.array(list(dic.keys()))
    values = np.array(list(dic.values()))

    # Get argsort indices
    sorted_idx = keys.argsort()
    # Drop the magic bomb with searchsorted to get the corresponding
    # places for a in keys (using sorter since a is not necessarily sorted).
    # Then trace it back to original order with indexing into sidx
    # Finally index into values for desired output.
    return values[sorted_idx[np.searchsorted(keys, array, sorter=sorted_idx)]]


def wait_for_reachability(session, url, max_retry=20, wait_time=3):
    """Wait for the api to be reachable by poking its healthz endpoint."""
    retry = 0
    logging.info("Waiting for the api to be reachable")
    while retry <= max_retry:
        try:
            resp = session.get(url + "/healthz")
        except (
            urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.TimeoutError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
        ):
            logging.info(".")
        else:
            if resp.ok:
                return True
        retry += 1
        sleep(wait_time)
    return False


def makeGrid(bounds, size):
    """Make polygon grid (adapted from: https://gis.stackexchange.com/a/316460)."""
    xmin, ymin, xmax, ymax = bounds

    wide = size
    length = size

    cols = list(np.arange(xmin, xmax + wide, wide))
    rows = list(np.arange(ymin, ymax + length, length))

    polygons = []
    for x in cols[:]:
        for y in rows[:]:
            polygons.append(
                Polygon(
                    [(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]
                )
            )

    grid = gpd.GeoDataFrame({"geometry": polygons})
    return grid


def getHDD(polygon, year=2020):
    """Get HeatinDegreeDays from EUROSTAT, or precomputed ones for Geneva."""
    df = []
    for month in range(1, 13):
        r = requests.post(
            POSTGREST_URL + POSTGREST_ENDPOINT,
            headers=HEADERS,
            json={
                "parameters": {
                    "data.ds_id": 9,
                    "start_at": "'{}-{}-01'".format(year, str(month).zfill(2)),
                    "intersecting": "{}".format(polygon.wkt),
                    "variable": "'Heating degree days'",
                    "level": "{NUTS3}",
                }
            },
        )
        if r.status_code != 200:
            raise ConnectionError(
                "There is a problem connecting to the EnerMaps API. Please try again"
                " later."
            )

        df.append(pd.DataFrame(r.json()))
    df = pd.concat(df, ignore_index=True)
    if df.shape[0] > 0:  # there are NUTS3 with HDD
        df["HDD"] = df["variables"].apply(lambda x: x["Heating degree days"])
        df["HDD_nosummer"] = df.loc[
            df.index.isin([0, 1, 2, 3, 4, 8, 9, 10, 11]), "HDD"
        ]  # used for the model
        response = (
            df.groupby("fid").sum().mean()[["HDD", "HDD_nosummer"]].values.tolist()
        )
        response.append(
            {
                "Warning": (
                    "The model has not been trained in this area. Please beware that"
                    " the results might not be reliable."
                )
            }
        )
        return response
    else:
        # Find the NUTS3 code
        r = requests.post(
            POSTGREST_URL + POSTGREST_ENDPOINT,
            headers=HEADERS,
            json={
                "parameters": {
                    "data.ds_id": 0,
                    "intersecting": "{}".format(polygon.wkt),
                    "level": "{NUTS3}",
                }
            },
        )
        if r.json()[0]["fid"] == "CH013":  # this is the Canton of Geneva
            CH013 = pd.read_csv("CH013_HDD.csv", index_col="time", parse_dates=True)
            response = CH013.loc[CH013.index.year == year, :].values.tolist()[0]
            response.append({"Warning": ""})
            return response
        else:
            raise ValueError("In this area Heating Degree Days are not available.")


def getFeatures(gdf):
    """Prepare features for rasterio.
    (source: https://automating-gis-processes.github.io/
    CSC18/lessons/L6/clipping-raster.html).
    """
    return [json.loads(gdf.to_json())["features"][0]["geometry"]]


def checkTile(matrix, tile_size):
    """Check whether tile complies with minimum requirements."""
    with open(os.path.join("models", MODELS[tile_size], "parameters.json"), "r") as f:
        parameters = json.loads(f.read())
    coverage_ratio = np.sum(matrix == 0) / np.sum(matrix >= 0)
    if coverage_ratio > parameters["idc_coverage_ratio"]:
        return True
    else:
        return False


def heatlearn(
    task,
    geojson,
    raster_paths,
    tile_size=500,
    year=2020,
):
    """Get heating demand from HeatLearn Model."""
    start = time()

    # Create boundary
    geometries = []
    for feature in geojson["features"]:
        geometry = feature["geometry"]
        geoshape = shape(geometry)
        geometries.append(geoshape)
    union_geometry = cascaded_union(geometries)
    boundary = gpd.GeoSeries(union_geometry)
    boundary = boundary.set_crs("EPSG:4326")
    boundary = boundary.to_crs("EPSG:3035")
    if boundary.area.sum() > MAX_AREA:
        raise ValueError("The selected area is too large.")
    boundary = gpd.GeoDataFrame(boundary)
    boundary = boundary.rename(columns={0: "geometry"}).set_geometry("geometry")

    # Make sure that the clipping geometry does not leave any pixel out
    boundary["geometry"] = boundary["geometry"].apply(
        lambda x: wkt.loads(wkt.dumps(x, rounding_precision=0))
    )
    offset = boundary.total_bounds % PIXEL_SIZE
    boundary["geometry"] = boundary["geometry"].translate(
        xoff=-offset[0], yoff=-offset[1]
    )

    # Make tiles
    bounds = boundary.total_bounds
    tiles = makeGrid(bounds, tile_size)
    tiles = tiles.set_crs("EPSG:3035")

    tiles = tiles.loc[tiles.intersects(boundary.iloc[0].geometry), :]
    tiles = tiles.reset_index()
    if tiles.shape[0] == 0:
        raise ValueError("No tiles were created.")

    # Prepare raster
    datasets = []

    for raster_path in raster_paths:
        src = rasterio.open(raster_path)
        datasets.append(src)

    meta = src.meta.copy()
    raster, out_trans = merge.merge(datasets)

    meta.update(
        {
            "driver": "GTiff",
            "height": raster.shape[1],
            "width": raster.shape[2],
            "transform": out_trans,
            "crs": "EPSG:3035",
        }
    )

    # Prepare inputs for the model
    # Initialize variables
    X = np.zeros(
        [tiles.shape[0], int(tile_size / PIXEL_SIZE), int(tile_size / PIXEL_SIZE), 2]
    )  # the second channel (mask) must have zeros
    tiles["suitable"] = False

    # Clip and check raster tiles
    with rasterio.io.MemoryFile() as memfile:
        with memfile.open(**meta) as dataset:
            dataset.write(raster)  # dataset with new encoding
            for t, row in tiles.iterrows():
                # Clipping geometry in Rasterio format
                coords = getFeatures(
                    gpd.GeoDataFrame({"geometry": row.geometry}, index=[0])
                )
                # Clip using rasterio
                out_img, out_transform = mask(
                    dataset=dataset, shapes=coords, crop=True, pad=0
                )
                matrix = np.squeeze(out_img)

                matrix = replace_with_dict(matrix)

                # Check suitability
                tiles.loc[t, "suitable"] = checkTile(matrix, tile_size)

                # Make sure that the Rasterio clipping is successful
                if 256 in np.unique(out_img):  # no 256-encoded pixels at borders
                    raise ValueError("Clipping was not succesful.")

                # Make sure each tile has the correct number of pixels
                if matrix.shape != (tile_size // 2.5, tile_size // 2.5):  # exact size
                    padded_array = np.zeros(
                        (int(tile_size // 2.5), int(tile_size // 2.5))
                    )
                    padded_array[: matrix.shape[0], : matrix.shape[1]] = matrix
                    matrix = padded_array
                    tiles.loc[t, "suitable"] = False
                X[t, :, :, 0] = matrix

    # Filter tiles
    X = X[tiles["suitable"], :, :, :]
    tiles = tiles.loc[tiles["suitable"], :]

    # Predictions
    model = load_model(os.path.join("models", MODELS[tile_size], "model"))
    preds = model.predict(X)
    clear_session()  # recover memory

    # Get HDD
    HDD, HDD_nosummer, warnings = getHDD(union_geometry, year=year)
    HDD_coeff = HDD_MODEL["slope"] * HDD_nosummer + HDD_MODEL["intercept"]

    # Adjust predictions
    preds = preds / HDD_coeff

    pred_done = time()

    # Prepare output
    # Vector output
    tiles["preds"] = preds
    grid = tiles.copy()
    grid["geometry"] = grid.centroid

    uid = uuid.uuid1()
    os.mkdir("tmp/{}".format(uid))
    dst_vector = "tmp/{}/vector.gpkg".format(uid)

    grid.to_file(dst_vector, driver="GPKG")

    # Rasterize vector grid
    dst_raster = "tmp/{}/raster.tif".format(uid)
    subprocess.run(  # nosec
        [
            "gdal_rasterize",
            "-a",
            "preds",
            "-tr",
            str(tile_size),
            str(tile_size),
            dst_vector,
            dst_raster,
        ],
    )

    raster_name = "result.tif"
    with open(dst_raster, mode="rb") as raster_fd:
        task.post_raster(raster_name=raster_name, raster_fd=raster_fd)

    # Remove temp files
    shutil.rmtree("tmp/{}".format(uid))

    # Dict return response
    ret = dict()
    ret["graphs"] = {}
    ret["geofiles"] = {"file": raster_name}
    ret["legend"] = createLegend(preds)
    if len(warnings["Warning"]) > 0:
        ret["warnings"] = warnings
    ret["values"] = {
        "Annual heating demand [GWh]": int(np.round(np.sum(preds) / 1000, 0)),
        "Heating density [MWh/ha]": int(
            np.round(np.sum(preds) / (tiles.shape[0] * (tile_size ** 2) * 0.0001), 0)
        ),
        "Heating Degree Days [°C]": int(np.round(HDD, 0)),
    }

    logging.info("We took {!s} to deploy the model".format(pred_done - start))
    validate(ret)
    return ret
