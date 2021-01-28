import logging
import os
from time import time
from typing import List, Optional, Text

import pyproj
import rasterio
from BaseCM.cm_output import validate
from rasterstats import zonal_stats
from shapely.geometry import shape
from shapely.ops import cascaded_union, transform
# print(os.environ)
# print("")
# print("")
# print(os.listdir("/usr/local/lib/python3.8/dist-packages/pyproj"))
#os.environ['PROJ_LIB'] = '/usr/local/share/proj'
# print(os.environ)
# print(os.environ)

GEOJSON_PROJ = "EPSG:4326"
DEFAULT_STATS = ("min", "max", "mean", "median", "count")
SCALED_STATS_PREFIX = ("min", "max", "mean", "median", "percentile_")
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

CDF_POINTS = range(0, 101)


def scale_stat(stats: dict, factor):
    """From a list of stats, take the factor into account and
    modify the stats accordingly.
    """
    for stat_name, stat in stats.items():
        for scaled_stat_prefix in SCALED_STATS_PREFIX:
            if stat and stat_name.startswith(scaled_stat_prefix):
                stats[stat_name] = stat * factor


def extract_graph(stats: dict):
    graph = []
    is_graph_invalid = False
    for cdf_point, percentile in zip(CDF_POINTS, get_cdf_stats()):
        percentile_step = stats[percentile]
        if percentile_step is None:
            is_graph_invalid = True
        graph.append(
            (
                stats[percentile],
                cdf_point,
            )
        )
        del stats[percentile]
    if is_graph_invalid:
        return []
    return graph


def get_cdf_stats():
    def to_percentile(percent):
        return "percentile_" + str(percent)

    return [to_percentile(percent) for percent in CDF_POINTS]


def rasterstats(geojson, raster_path, factor, stat_types: Optional[List[Text]] = None):
    """Multiply the rasters values by a factor.

    Rasters are selected from the frontend.
    Factor should be an integrer.
    By default, the indicators are "count min mean max median".
    """
    if not stat_types:
        stat_types = DEFAULT_STATS
    stat_types = list(stat_types)
    stat_types += get_cdf_stats()
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
    stats = zonal_stats(
        merged_geometries, raster_path, affine=src.transform, stats=stat_types
    )
    # we have a single feature, thus we expose a single stat
    if len(stats):
        stat = stats[0]
    else:
        stat = {}
    scale_stat(stat, factor)
    graph = extract_graph(stat)

    stat_done = time()
    ret = dict()
    ret["graphs"] = {}
    if graph:
        ret["graphs"]["cdf"] = {}
        ret["graphs"]["cdf"]["type"] = "xy"
        ret["graphs"]["cdf"]["values"] = graph
    ret["geofiles"] = {}
    ret["values"] = stat

    logging.info("We took {!s} to calculate stats".format(stat_done - start))
    validate(ret)
    return ret
