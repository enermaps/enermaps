import logging
import uuid

from BaseCM.cm_output import output_raster
from requests.exceptions import ConnectionError


def process(file):
    try:
        status = output_raster(
            "frontend_name_" + str(uuid.uuid1()) + ".tif", open(file, "rb")
        )
        return status
    except ConnectionError:
        logging.error("Error during the post of the file.")
        return False
