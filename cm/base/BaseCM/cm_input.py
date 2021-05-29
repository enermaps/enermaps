import os

import pyproj
from shapely.geometry import shape
from shapely.ops import cascaded_union, transform

import rasterio
from BaseCM.cm_output import validate
from rasterstats import zonal_stats

GEOJSON_PROJ = "EPSG:4326"


def get_raster_path(raster_name):
    """Returns the path to the raster file based on the raster name."""
    raster_dir = os.path.join(os.environ["UPLOAD_DIR"], "raster")
    raster_path = os.path.join(raster_dir, raster_name, "raster.tiff")
    return raster_path


class StatNotComputeError(Exception):
    """Exception thrown for a non-existing calculation module"""

    pass


def validate_selection(
    selection: dict,
    raster: str,
):
    """
    Find the number of count for given a raster and a area selection in order to define if the
    selection is valid or not.

    Inputs:
        * raster : path to the raster selected from the frontend.
        * selection : area selection made from the frontend
    Outputs:
        * selection_valid : boolean that define if raster selection is valid.
        * response : response return to the front end when are selected is not valid.
    """
    with rasterio.open(raster) as src:
        project = pyproj.Transformer.from_crs(
            GEOJSON_PROJ, src.crs, always_xy=True
        ).transform

    try:
        features = selection["features"]
    except:
        raise KeyError("GEOJSON does not have features key.")

    geometries = []
    for feature in features:
        try:
            geometry = feature["geometry"]
        except:
            raise KeyError("GEOJSON does not have geometry key.")
        geoshape = shape(geometry)
        projected_shape = transform(project, geoshape)
        geometries.append(projected_shape)
    merged_geometries = cascaded_union(geometries)
    stats = zonal_stats(merged_geometries, raster, affine=src.transform, stats="count")

    try:
        count = stats[0]["count"]
    except:
        raise StatNotComputeError(f"Statistics not compute: {stats}")

    if count > 0:
        selection_valid = True
        response = None
    else:
        selection_valid = False
        response = dict()
        response["graphs"] = {}
        response["geofiles"] = {}
        response["values"] = {"Selection not valid - Count :": 0}
        validate(response)

    return selection_valid, response
