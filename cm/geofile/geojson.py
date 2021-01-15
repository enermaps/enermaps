import os
import uuid

import requests

from rasterstats import zonal_stats

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTDATA_DIR = os.path.join(CURRENT_DIR, "testdata")
TEST_FILE = os.path.join(TESTDATA_DIR, "small_test.tif")


def post_geofile(file):
    files = {
        "file": (
            "frontend_name_" + str(uuid.uuid1()) + ".tif",
            open(file, "rb"),
            "image/geotiff",
        ),
    }
    try:
        response = requests.post("http://127.0.0.1:7000/api/geofile/", files=files)
        print(response.status_code)
    except requests.exceptions.ConnectionError:
        print("ERROR in the post.")


def process(vectors, raster):
    dev_mode = True
    if not dev_mode:
        res = zonal_stats(vectors=vectors, raster=raster, prefix="cm_", raster_out=True)
        res = res[0]["cm_mini_raster_array"]
        print(res)
        print(type(res))
    post_geofile(file=TEST_FILE)
