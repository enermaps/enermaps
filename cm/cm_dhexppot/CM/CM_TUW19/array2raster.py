"""
Created on August 14 2018

@author: fallahnejad@eeg.tuwien.ac.at
"""
import os
import sys
import time
import numpy as np
from osgeo import gdal
from osgeo import osr
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def array2raster(outRasterPath, geo_transform, dataType, array, noDataValue=0,
                 OutputRasterSRS=3035):
    '''
    This function rasterizes the input numpy array. The input array and the
    geo_transform must be given for EPSG3035.
    '''
    # conversion of data types from numpy to gdal
    dict_varTyp = {"int8":      gdal.GDT_Byte,
                   "int16":     gdal.GDT_Int16,
                   "int32":     gdal.GDT_Int32,
                   "uint16":    gdal.GDT_UInt16,
                   "uint32":    gdal.GDT_UInt32,
                   "float32":   gdal.GDT_Float32,
                   "float64":   gdal.GDT_Float64}
    cols = array.shape[1]
    rows = array.shape[0]
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(outRasterPath, cols, rows, 1,
                              dict_varTyp[dataType], ['compress=DEFLATE',
                                                      'TILED=YES',
                                                      'TFW=YES',
                                                      'ZLEVEL=9',
                                                      'PREDICTOR=1'])
    outRaster.SetGeoTransform(geo_transform)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(OutputRasterSRS)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outRaster.GetRasterBand(1).SetNoDataValue(noDataValue)

    if dataType == 'int8' or dataType == 'uint16':
        # This can be used for dtype int8
        ct = gdal.ColorTable()
        ct.SetColorEntry(noDataValue, (0, 0, 0, 255))
        ct.SetColorEntry(1, (250, 159, 181, 255))
        '''
        for i in range(1, 1+np.max(array)):
            ct.SetColorEntry(i, tuple(np.random.choice(range(256), size=4)))
        '''
        outRaster.GetRasterBand(1).SetColorTable(ct)

    outRaster.GetRasterBand(1).WriteArray(array)
    outRaster.FlushCache()
