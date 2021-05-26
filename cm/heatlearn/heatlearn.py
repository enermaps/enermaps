import logging
import os
from time import sleep, time

import numpy as np
import rasterio
import requests
import urllib3
from BaseCM.cm_output import validate
from matplotlib import pyplot as plt

# from rasterstats import zonal_stats
from shapely.geometry import shape
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

MODEL_UUID = "5d7493b6-9705-11eb-b3f9-3e22fb3fc3ab"


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


def heatlearn(geojson, raster_path, tile_size):
    """Get heating demand from HeatLearn Model
    """
    start = time()

    geometries = []
    for feature in geojson["features"]:
        geometry = feature["geometry"]
        geoshape = shape(geometry)
        geometries.append(geoshape)

    matrix = plt.imread(raster_path)
    matrix = replace_with_dict(matrix)

    mask = np.zeros(matrix.shape)

    X = np.zeros([1, matrix.shape[0], matrix.shape[1], 2])
    X[0, :, :, 0] = matrix
    X[0, :, :, 1] = mask

    model = load_model(os.path.join("models", MODEL_UUID, "model"))
    preds = model.predict(X)

    stat_done = time()
    ret = dict()
    ret["graphs"] = {}

    ret["geofiles"] = {"file": "tmp/tmp.tif"}
    ret["values"] = {"results": float(preds[0][0])}

    with rasterio.open(raster_path) as src:
        transform = src.transform
    transform_500 = rasterio.Affine(
        500, transform[1], transform[2], transform[3], -500, transform[5]
    )
    with rasterio.open(
        "tmp/tmp.tif",
        "w",
        driver="GTiff",
        height=1,
        width=1,
        count=1,
        transform=transform_500,
        dtype=np.float32,
        crs="EPSG:2056",  # provisionally to CH1903+ as the source
    ) as src:
        src.write(np.array(preds[0][0]).reshape(1, 1, 1))

    with open("tmp/tmp.tif", "rb") as f:
        # output_raster("out.tif",f)
        files = {"file": ("out.tif", f, "image/tiff")}
        session = requests.Session()
        if not wait_for_reachability(session, "http://api"):
            logging.error("API is not reachable after max retries")
        else:
            session.delete("http://api/api/geofile/out.tif")
            session.post("http://api/api/geofile", files=files)

    logging.info("We took {!s} to deploy the model".format(stat_done - start))
    validate(ret)
    return ret
