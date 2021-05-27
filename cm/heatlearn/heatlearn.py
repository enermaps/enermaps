import json
import logging
import os
from time import sleep, time

import geopandas as gpd
import numpy as np
import rasterio
import requests
import urllib3
from BaseCM.cm_output import validate
from geocube.api.core import make_geocube
from matplotlib import pyplot as plt
from rasterio.mask import mask
from shapely import wkt
from shapely.geometry import Polygon, shape
from shapely.ops import cascaded_union
from tensorflow.keras.models import load_model

logging.basicConfig(level=logging.INFO)


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


def replace_with_dict(ar: np.array, dic: dict = ESM_dict):
    """Replace numpy values with dict (source: https://stackoverflow.com/a/47171600)."""
    #
    # Extract out keys and values
    k = np.array(list(dic.keys()))
    v = np.array(list(dic.values()))

    # Get argsort indices
    sidx = k.argsort()

    # Drop the magic bomb with searchsorted to get the corresponding
    # places for a in keys (using sorter since a is not necessarily sorted).
    # Then trace it back to original order with indexing into sidx
    # Finally index into values for desired output.
    return v[sidx[np.searchsorted(k, ar, sorter=sidx)]]


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
    for x in cols[:-1]:
        for y in rows[:-1]:
            polygons.append(
                Polygon(
                    [(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]
                )
            )

    grid = gpd.GeoDataFrame({"geometry": polygons})
    return grid


def heatlearn(geojson, raster_paths, tile_size):
    """Get heating demand from HeatLearn Model."""
    assert tile_size in [500, 300]
    pixel_size = 2.5
    start = time()

    # Create boundary
    geometries = []
    for feature in geojson["features"]:
        geometry = feature["geometry"]
        geoshape = shape(geometry)
        geometries.append(geoshape)
    boundary = gpd.GeoSeries(cascaded_union(geometries))
    boundary = boundary.set_crs("EPSG:4326")
    boundary = boundary.to_crs("EPSG:3035")
    boundary = gpd.GeoDataFrame(boundary)
    boundary = boundary.rename(columns={0: "geometry"}).set_geometry("geometry")
    assert boundary.shape[0] == 1

    # Make sure that the clipping geometry does not leave any pixel out
    boundary["geometry"] = boundary["geometry"].apply(
        lambda x: wkt.loads(wkt.dumps(x, rounding_precision=0))
    )
    offset = boundary.total_bounds % pixel_size
    boundary["geometry"] = boundary["geometry"].translate(
        xoff=-offset[0], yoff=-offset[1]
    )

    # Make tiles
    bounds = boundary.total_bounds
    tiles = makeGrid(bounds, tile_size)
    tiles = tiles.set_crs("EPSG:3035")
    logging.info(boundary.geometry)
    logging.info(tiles.total_bounds)
    tiles = tiles.loc[tiles.intersects(boundary.iloc[0].geometry), :]
    tiles = tiles.reset_index()
    assert tiles.shape[0] > 0

    # Prepare raster
    if len(raster_paths) == 1:
        raster_path = raster_paths[0]
    else:
        pass  # TBD: Use Rasterio to merge rasters
    with rasterio.open(raster_path) as dataset:
        raster = dataset.read()
        meta = dataset.meta
        raster = replace_with_dict(raster)
        raster = raster.astype(np.uint16)

    def getFeatures(gdf):
        """Prepare features for rasterio (source: https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html)."""
        return [json.loads(gdf.to_json())["features"][0]["geometry"]]

    # Prepare inputs for the model
    X = np.zeros(
        [tiles.shape[0], int(tile_size / pixel_size), int(tile_size / pixel_size), 2]
    )  # the second channel (mask) must have zeros

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
                # Make sure that the Rasterio clipping is successful
                assert 256 not in np.unique(out_img)  # no 256-encoded pixels at borders
                assert matrix.shape == (tile_size / 2.5, tile_size / 2.5)  # exact size
                X[t, :, :, 0] = matrix

    # Predictions
    model = load_model(os.path.join("models", MODELS[tile_size], "model"))
    preds = model.predict(X)

    pred_done = time()

    # Prepare output
    # Raster output
    tiles["preds"] = preds
    cube = make_geocube(
        vector_data=tiles,
        measurements=["preds"],
        resolution=(-tile_size, tile_size),
        output_crs="EPSG:3035",
    )
    cube["preds"].rio.to_raster("tmp/tmp.tif")

    # Colorize
    os.system("gdaldem color-relief -alpha tmp/tmp.tif colors.txt tmp/tmp_rgb.tif")

    with open("tmp/tmp_rgb.tif", "rb") as f:
        files = {"file": ("out.tif", f, "image/tiff")}
        session = requests.Session()
        if not wait_for_reachability(session, "http://api"):
            logging.error("API is not reachable after max retries")
        else:
            session.delete("http://api/api/geofile/out.tif")
            session.post("http://api/api/geofile", files=files)

    # Dict return response
    ret = dict()
    ret["graphs"] = {}

    ret["geofiles"] = {"file": "tmp/tmp_rgb.tif"}
    ret["values"] = {"results": int(np.round(np.sum(preds), 0))}

    logging.info("We took {!s} to deploy the model".format(pred_done - start))
    validate(ret)
    return ret
