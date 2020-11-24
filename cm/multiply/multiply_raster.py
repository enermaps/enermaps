import logging
from time import time

import rasterio
from rasterstats import zonal_stats


def MultiplyRasterStats(geojson, rasters, factor):
    """Multiply the rasters values by a factor.
    Rasters are selected from the frontend.
    Factor should be an integrer.
    """
    with rasterio.open(rasters) as src:
        raster_array = src.read(1) * factor
    fetch_done = time()
    stats = zonal_stats(geojson, raster_array, affine=src.transform)
    stat_done = time()

    logging.info(
        "DOUBLE - Fetching and doubling raster time : ", fetch_done - now, " s"
    )
    logging.info("DOUBLE - Statistic processing time : ", stat_done - fetch_done, " s")
    logging.info("DOUBLE - Overall execution time : ", stat_done - now, " s")
    logging.info(stats)
    return stats


if __name__ == "__main__":
    val_multiply = MultiplyRasterStats(
        "selection_shapefile.geojson", "GeoTIFF_test.tif"
    )
    print(val_multiply)
