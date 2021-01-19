import logging
import uuid
from requests.exceptions import ConnectionError
from BaseCM.cm_output import output_raster


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
    except :
        print("ERROR in the post.")


def process(file):
    try:
        status = output_raster("frontend_name_" + str(uuid.uuid1()) + ".tif", open(file, "rb"))
        return status
    except ConnectionError:
        logging.error("Error during the post of the file.")
        return False
