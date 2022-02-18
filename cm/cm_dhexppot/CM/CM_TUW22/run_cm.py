import os
import time
import sys
from osgeo import gdal

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW22.clip import clip_raster as cr
from CM.CM_TUW1.read_raster import raster_array as RA


def main(
    rast,
    features_path,
    output_dir,
    gt,
    nodata=-9999,
    save2csv=None,
    save2raster=None,
    save2shp=None,
    unit_multiplier=None,
    return_array=False,
    OutputSRS=3035,
):
    output = cr(
        rast,
        features_path,
        output_dir,
        gt,
        nodata,
        save2csv,
        save2raster,
        save2shp,
        unit_multiplier,
        return_array,
        OutputSRS,
    )
    if return_array:
        return output


if __name__ == "__main__":
    start = time.time()
    # path to the src
    data_warehouse = path + os.sep + "AD/data_warehouse"
    features_path = data_warehouse + os.sep + "AT_NUTS3.shp"
    raster = data_warehouse + os.sep + "heat_tot_curr_density_AT.tif"
    output_dir = path + os.sep + "Outputs"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    nodata = 0
    rast, gt = RA(raster, return_gt=True)
    cr(
        rast,
        features_path,
        output_dir,
        gt,
        save2raster=True,
        save2shp=True,
        save2csv=True,
        return_array=True,
        nodata=0,
    )
    elapsed = time.time() - start
    print("%0.3f seconds" % elapsed)
