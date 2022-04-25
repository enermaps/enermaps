import logging
import os
from time import time
from typing import List, Optional, Text

import pyproj
import rasterio
from BaseCM.cm_output import validate
from rasterstats import zonal_stats
from shapely.geometry import shape
from shapely.ops import transform, unary_union

GEOJSON_PROJ = "EPSG:4326"
DEFAULT_STATS = ("min", "max", "mean", "median", "count")
SCALED_STATS_PREFIX = ("min", "max", "mean", "median", "percentile_")
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

CDF_POINTS = range(0, 101)
OUTPUT_PRECISION = 3


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


def rasterstats(geojson: dict, raster_path: str, factor: int, stat_types: Optional[List[Text]] = None) -> dict:
    """
    Multiply the rasters values by a factor and return statistics about this new .

    Inputs :
        * geojson : area of the raster to consider.
        * raster_path : path to the raster.
        * factor : the multiplication factor (it should be an integrer).
        * stat_types : statistics (or indicators) to be returned
        (by default, the indicators are "count min mean max median".

    Output :
        * Response for the frontend containing :
            * values of the indicators
            * values mandatory for drawing de chart
    """

    def rounded_statistics(statistics: dict, accuracy: int = OUTPUT_PRECISION ) -> dict:
        """
        Take statistical data and round it to a given precision.

        Inputs :
            * statistics : Statistical data.
            * accuracy : Number of decimals.

        Output :
            * Rounded statistical data.
        """
        if not isinstance(statistics, dict):
            TypeError("A dictionary is expected.")
        values = dict()
        for key, value in statistics.items():
            if value is not None:
                values[key] = round(value, accuracy)
        return values

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
    merged_geometries = unary_union(geometries)
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
    ret["values"] = rounded_statistics(statistics=stat)
    ret["graphs"] = list()
    if graph:
        ret["graphs"].append(dict())
        ret["graphs"][0]["cumulative distribution graph"] = {}
        ret["graphs"][0]["cumulative distribution graph"]["type"] = "xy"
        ret["graphs"][0]["cumulative distribution graph"]["values"] = graph

    ret["geofiles"] = dict()

    logging.info("We took {!s} to calculate stats".format(stat_done - start))
    res = validate(ret)
    return res
