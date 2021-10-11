import logging
import os

import geojson
import pyproj
import rasterio
import shapely
from BaseCM.cm_output import validate
from rasterstats import zonal_stats
from shapely.geometry import shape
from shapely.ops import cascaded_union, transform

GEOJSON_PROJ = "EPSG:4326"


def get_raster_path(raster_name):
    """Returns the path to the raster file based on the raster name."""
    raster_dir = os.path.join(os.environ["WMS_CACHE_DIR"], "raster")
    raster_path = os.path.join(raster_dir, raster_name, "raster.tiff")
    return raster_path


class StatNotComputeError(Exception):
    """Exception thrown when it's not possible to calculate the statistics."""

    pass


def validate_selection(
    selection: dict,
    raster: str,
    max_count: int = None,
):
    """
    Find the number of counts for a given raster and area selection to define
    whether the selection is valid or not.
    The count is a non-null pixel of a raster.

    Inputs:
        * raster : selected raster from the frontend.
        * selection : selected area from the frontend
    Outputs:
        * selection_valid : boolean that defines if the selection is valid.
        * response : dictionary of the validation result
    """
    with rasterio.open(raster) as src:
        project = pyproj.Transformer.from_crs(
            GEOJSON_PROJ, src.crs, always_xy=True
        ).transform

    try:
        features = selection["features"]
    except KeyError:
        logging.error("Selection does not have any feature.")

    geometries = []
    for feature in features:
        try:
            geometry = feature["geometry"]
        except KeyError:
            logging.error("Feature does not have geometry key.")
        geoshape = shape(geometry)
        projected_shape = transform(project, geoshape)
        geometries.append(projected_shape)
    merged_geometries = cascaded_union(geometries)
    stats = zonal_stats(merged_geometries, raster, affine=src.transform, stats="count")

    try:
        count = stats[0]["count"]
    except KeyError:
        raise StatNotComputeError(f"Statistics not compute: {stats}")

    response = dict()
    response["graphs"] = {}
    response["geofiles"] = {}
    response["values"] = {}
    selection_valid = False
    if count <= 0:
        response["values"] = {"No count found:": 0}
    else:
        if max_count is not None and count > max_count:
            response["values"] = {
                "Too many count found (max." + str(max_count) + "):": str(count)
            }
        else:
            selection_valid = True
    validate(response)
    return selection_valid, response


def merged_polygons(selection: dict) -> dict:
    merged_polygon = shapely.geometry.polygon.Polygon()
    region = selection["features"]
    n_polygon = len(region)

    for i in range(n_polygon):
        poly_to_add = shapely.geometry.asShape(region[i]["geometry"])
        merged_polygon = merged_polygon.union(poly_to_add)
    geojson_out = geojson.Feature(geometry=merged_polygon, properties={})
    return geojson_out.geometry
