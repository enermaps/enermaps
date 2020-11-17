import os

from flask import send_file
from flask_restx import Namespace, Resource

from rasterstats import zonal_stats
import rasterio
from time import time
import numpy as np

api = Namespace("cm", "Calculation module endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))
file_test_dir = os.path.join(os.path.dirname(current_file_dir), 'test_file')

#@api.route("/<int:id_cm>/task/<int:task_id>")
@api.route("/0/task/0")
class CM_fakeoutput(Resource):
    def get(self):
        fakeoutput = os.path.join(current_file_dir, "fakeoutput.json")
        return send_file(fakeoutput)

@api.route("/0/task/1")
class CM_fakeoutput(Resource):
    def get(self):
        #GEOJSON_PROJ = 'EPSG:4326'
        #PROJ_4326 = 'EPSG:4326'
        #PROJ_2056 = 'EPSG:2056'
        def add_rasterstats(path_geojson = os.path.join(file_test_dirr, "selection_shapefile.geojson"),
                            path1 = os.path.join(file_test_dirr, "GeoTIFF_test.tif"),
                            path2 = os.path.join(file_test_dirr, "GeoTIFF_test.tif"),
                            evaluate = False):
            now = time()
            with rasterio.open(path1) as src1, rasterio.open(path2) as src2:
                raster1_array = src1.read(1)
                raster2_array = src2.read(1)
            fetch_done = time()
            rasterResult_array = np.add(raster1_array, raster2_array)
            add_done = time()
            stats = zonal_stats(path_geojson, rasterResult_array, affine=src1.transform)
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
        crs, stats = add_rasterstats()
        return stats[0]

@api.route("/0/task/2")
class CM_fakeoutput(Resource):
    def get(self):
        def double_rasterstats(path_geojson = os.path.join(file_test_dirr, "selection_shapefile.geojson"),
                               path = os.path.join(file_test_dirr, "GeoTIFF_test.tif"),
                               factor = 2,
                               evaluate = False):
            now = time()
            with rasterio.open(path) as src:
                raster_array = src.read(1) * factor
            fetch_done = time()
            stats = zonal_stats(path_geojson, raster_array, affine=src.transform)
            stat_done = time()
            if evaluate:
                print('DOUBLE - Fetching and doubling raster time : ', fetch_done - now, ' s')
                print('DOUBLE - Statistic processing time : ', stat_done - fetch_done, ' s')
                print('DOUBLE - Overall execution time : ', stat_done - now, ' s')
            else:
                print('DOUBLE - Execution time : ', stat_done - now, ' s')
                print(stats)
            return src.crs, stats
        crs, stats = double_rasterstats()
        return stats[0]

@api.route("/0/task/3")
class CM_fakeoutput(Resource):
    def get(self):
        def reproject_rasterstats(path_geojson = os.path.join(file_test_dirr, "selection_shapefile.geojson"),
                                  path_tif = os.path.join(file_test_dirr, "GeoTIFF_test_2056.tif"),
                                  evaluate = False):
            with rasterio.open(path_tif) as src:
                now = time()
                transform, width, height = calculate_default_transform(
                    src.crs, GEOJSON_PROJ, src.width, src.height, *src.bounds)
                kwargs = src.meta.copy()
                kwargs.update({
                    'crs': GEOJSON_PROJ,
                    'transform': transform,
                    'width': width,
                    'height': height})
                fetch_done = time()
                raw_dst = MemoryFile()
                with raw_dst.open(drive='GTiff', **kwargs) as dst:
                    for i in (1,):  # range(1, src.count + 1):
                        reproject(
                            source=rasterio.band(src, i),
                            destination=rasterio.band(dst, i),
                            src_transform=src.transform,
                            src_crs=src.crs,
                            dst_transform=transform,
                            dst_crs=GEOJSON_PROJ)
                        proj_done = time()
                        stats = zonal_stats(path_geojson, dst.read(1), affine=dst.transform)
                        stat_done = time()
            if evaluate:
                print('REPROJ - Fetching raster time : ', fetch_done - now, ' s')
                print('REPROJ - Raster reprojection time : ', proj_done - fetch_done, ' s')
                print('REPROJ - Statistic processing time : ', stat_done - proj_done, ' s')
                print('REPROJ - Overall execution time : ', stat_done - now, ' s')
            else:
                print('REPROJ - Execution time : ', stat_done - now, ' s')
                print(stats)
            return dst.crs, stats
        crs, stats = reproject_rasterstats()
        return stats[0]