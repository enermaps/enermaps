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


def epsg_from_geotiff(path):
    """Extract the proj4 formatted projection descrition
    from a geotiff file.
    """
    raster = gdal.Open(path)
    if not raster:
        return None

    prj = raster.GetProjection()
    prj = prj.strip()
    if not prj:
        return None

    srs = osr.SpatialReference(wkt=prj)

    if srs.GetAuthorityName(None) != "EPSG":
        return None

    return srs.GetAuthorityName(None) + ":" + srs.GetAuthorityCode(None)


def epsg_to_wkt(epsg_code: int) -> str:
    """Return a wkt description from an epsg integer
    code
    """
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg_code)
    return srs.ExportToWkt()


def epsg_string_to_epsg(epsg_string: str) -> int:
    """From a string of the form 'EPSG:${code}' return
    the epsg code as a integer
    Raise a ValueError if the epsg_string cannot
    be decoded
    """
    epsg_string = epsg_string.lower()
    epsg_string = epsg_string.strip()
    epsg_string = epsg_string.replace("epsg:", "")

    return int(epsg_string)


def epsg_to_proj4(epsg_code: int) -> str:
    """Craft a proj4 string from a epsg code as an integer
    this is actually pretty simple as epsg code can be
    expressed as proj4
    """
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg_code)
    return srs.ExportToProj4()


def epsg_string_to_proj4(epsg_string: str) -> str:
    """from an epsg string in the form "EPSG:${code}
    return the proj4 format.
    """
    epsg = epsg_string_to_epsg(epsg_string)
    return epsg_to_proj4(epsg)
