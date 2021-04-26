import os


def get_raster_path(raster_name):
    """Returns the path to the raster file based on the raster name."""
    raster_dir = os.path.join(os.environ["UPLOAD_DIR"], "raster")
    raster_path = os.path.join(raster_dir, raster_name, "raster.tiff")
    return raster_path
