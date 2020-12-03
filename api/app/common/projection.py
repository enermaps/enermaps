"""Set of function for extracting projection from file
and changing projection from one format to another.


This link gives a good introduction to coordinate description formats:
https://www.earthdatascience.org/courses/use-data-open-source-python/intro-vector-data-python/spatial-data-vector-shapefiles/epsg-proj4-coordinate-reference-system-formats-python/
"""
import glob
import os

import gdal
import osr
from flask import current_app


def proj4_from_shapefile(path):
    """Extract the proj4 formatted projection description
    from a extracted shapefile. This function will look
    for a prj file then map the content of that file
    to a proj4 string description.
    """
    proj_files = glob.glob(os.path.join(path, "*prj"))
    if not proj_files:
        return ""
    proj_file = proj_files[0]
    try:
        with open(proj_file) as f:
            wkt = f.read(current_app.config["MAX_PROJECTION_LENGTH"])
    except FileNotFoundError:
        return ""
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    return srs.ExportToProj4()


def proj4_from_geotiff(path):
    """Extract the proj4 formatted projection descrition
    from a geotiff file.
    """
    raster = gdal.Open(path)
    if not raster:
        return ""
    prj = raster.GetProjection()
    prj = prj.strip()
    if not prj:
        return ""
    srs = osr.SpatialReference(wkt=prj)

    return srs.ExportToProj4()


def epsg_to_wkt(epsg_code: int):
    """Map a integer epsg code to a wkt projection."""
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg_code)
    return srs.ExportToWkt()
