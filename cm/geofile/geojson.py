import uuid

from BaseCM.cm_output import output_raster


def process(file):
    status = output_raster(
        "frontend_name_" + str(uuid.uuid1()) + ".tif", open(file, "rb")
    )
    return status

