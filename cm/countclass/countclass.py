import logging
import os
from time import time
from typing import List, Optional, Text
import numpy as np
import pyproj
import rasterio
import rasterio.mask
from BaseCM.cm_output import validate
# from rasterstats import zonal_stats
from shapely.geometry import shape
from shapely.ops import cascaded_union, transform

GEOJSON_PROJ = "EPSG:4326"


def calculate(geojson, raster_path, rasterclass):
    """Get the area of the rasterclass.

    Rasters are selected from the frontend.
    """

    start = time()
    with rasterio.open(raster_path) as src:
        project = pyproj.Transformer.from_crs(
            GEOJSON_PROJ, src.crs, always_xy=True
        ).transform
    geometries = []
    for feature in geojson["features"]:
        geometry = feature["geometry"]
        geoshape = shape(geometry)
        projected_shape = transform(project, geoshape)
        geometries.append(projected_shape)
    merged_geometries = cascaded_union(geometries)

    with rasterio.open(raster_path) as src:
        raster, raster_transform = rasterio.mask.mask(src, [merged_geometries], crop=True)
        print(src.meta)
        gt = src.meta["transform"]
        width = src.meta["width"]
        height = src.meta["height"]
    pixelSizeX = gt[0]
    pixelSizeY =-gt[4]

    area = np.sum(raster == rasterclass)*pixelSizeX*pixelSizeY
    stat = [np.round(area/1e+6,2), #area
            np.round((area/projected_shape.area)*100,2) #percentage
        ]
    stat_done = time()
    ret = dict()
    ret["graphs"] = []
    ret["geofiles"] = []
    ret["values"] = stat

    logging.info("We took {!s} to calculate the area".format(stat_done - start))

    validate(ret)
    return ret
