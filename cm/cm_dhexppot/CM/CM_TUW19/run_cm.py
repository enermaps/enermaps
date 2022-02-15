'''
Created on Jul 26, 2017

@author: simulant
'''
import os
import time
import sys
import numpy as np
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
import CM.CM_TUW19.array2raster as A2R


def main(outRasterPath, geo_transform, dataType, array, noDataValue=0,
         OutputRasterSRS=3035):
    A2R.array2raster(outRasterPath, geo_transform, dataType, array,
                     noDataValue, OutputRasterSRS)
    return

if __name__ == "__main__":
    start = time.time()
    output_dir = path + os.sep + 'Outputs'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    outRasterPath = output_dir + os.sep + 'array2raster.tif'
    array = np.ones((50, 20))
    dataType = 'float32'
    geo_transform = (4285400, 100, 0, 2890500, 0, -100)
    noDataValue = 0
    main(outRasterPath, geo_transform, dataType, array, noDataValue)
    elapsed = time.time() - start
    print("%0.3f seconds" % elapsed)
