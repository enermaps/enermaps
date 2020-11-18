from rasterstats import zonal_stats
import rasterio
from time import time
import logging


def MultiplyRasterstats(path_geojson, path, factor):
    now = time()
    with rasterio.open(path) as src:
        raster_array = src.read(1)*factor
    fetch_done = time()
    stats = zonal_stats(path_geojson, raster_array, affine=src.transform)
    stat_done = time()

    logging.info('DOUBLE - Fetching and doubling raster time : ', fetch_done - now, ' s')
    logging.info('DOUBLE - Statistic processing time : ', stat_done - fetch_done, ' s')
    logging.info('DOUBLE - Overall execution time : ', stat_done - now, ' s')
    logging.info(stats)
    return stats

if __name__ == "__main__":
    val_multiply = multiply_rasterstats("selection_shapefile.geojson", "GeoTIFF_test.tif")
    print(val_multiply)
