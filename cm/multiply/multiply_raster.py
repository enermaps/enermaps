from rasterstats import zonal_stats
import rasterio
from time import time


def MultiplyRasterstats(path_geojson, path, factor = 2, evaluate = False):
    now = time()
    with rasterio.open(path) as src:
        raster_array = src.read(1)*factor
    fetch_done = time()
    stats = zonal_stats(path_geojson, raster_array, affine=src.transform)
    stat_done = time()
    if evaluate:
        print('DOUBLE - Fetching and doubling raster time : ', fetch_done - now, ' s')
        print('DOUBLE - Statistic processing time : ', stat_done - fetch_done, ' s')
        print('DOUBLE - Overall execution time : ', stat_done - now, ' s')
        print(stats)
    return stats

if __name__ == "__main__":
    val_multiply = multiply_rasterstats("selection_shapefile.geojson", "GeoTIFF_test.tif")
    print(val_multiply)
