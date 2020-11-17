import os

from flask import send_file
from flask_restx import Namespace, Resource

from rasterstats import zonal_stats
import rasterio
from time import time
import numpy as np

api = Namespace("cm_zonalstat", "Calculation module endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))


@api.route("/<int:id_cm>/task/<int:task_id>")
class CM_fakeoutput(Resource):
    def get(self, id_cm, task_id):
        GEOJSON_PROJ = 'EPSG:4326'
        PROJ_4326 = 'EPSG:4326'
        PROJ_2056 = 'EPSG:2056'
        def add_rasterstats(path_geojson, path1, path2, evaluate=False):
            now = time()
            with rasterio.open(path1) as src1, rasterio.open(path2) as src2:
                raster1_array = src1.read(1)
                raster2_array = src2.read(1)
            fetch_done = time()
            rasterResult_array = np.add(raster1_array, raster2_array)
            add_done = time()
            stats = zonal_stats(path_geojson,
                                rasterResult_array, affine=src1.transform)
            stat_done = time()
            if evaluate:
                print('ADD - Fetching raster time : ', fetch_done - now, ' s')
                print('ADD - Raster reprojection time : ', add_done - fetch_done, ' s')
                print('ADD - Statistic processing time : ', stat_done - proj_done, ' s')
                print('ADD - Overall execution time : ', stat_done - now, ' s')
            else:
                print('ADD - Execution time : ', stat_done - now, ' s')
                print(stats)

            return src1.crs, stats

        if __name__ == "__main__":
            crs, val_added = add_rasterstats("selection_shapefile.geojson",
                                             "GeoTIFF_test.tif", "GeoTIFF_test.tif")
            print(crs, val_added)