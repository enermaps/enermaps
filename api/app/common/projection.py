import glob
import os
from typing import Text

import gdal
import osr
from flask import current_app


def proj4_from_shapefile(path):
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
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg_code)
    return srs.ExportToWkt()
