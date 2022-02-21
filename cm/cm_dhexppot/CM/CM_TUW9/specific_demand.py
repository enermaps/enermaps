# -*- coding: utf-8 -*-
"""
Created on June 8 2017

@author: fallahnejad@eeg.tuwien.ac.at
"""
import os
import shutil
import sys
import time

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
"""
- This code only should be run when the specific demand values of the countries
were changed. Otherwise, the corresponding outputs exist in the data warehouse.
Subsequent to running this code, the obtained rasters should be input to the
other codes within CM_TUW9.
- This code reads the CSV file containing specific demand values of buildings
in each EU country [kWh/m2/a] and creates a shapefile with a NUTS3 code field
as well as all demand columns within the CSV file. The first row of the CSV
file should be the header. For this purpose, an empty EU Shapefile is required.
Subsequently, the obtained shapefile is rasterized for further calculation
purposes.
- In the input CSV file, the name of columns corresponding to the specific
demand MUST be "Residential" and "Service". This is because the other modules
use the outputs of this module and expect these names for the outputs.
"""


def gdal_rasterize(
    vector_fn,
    raster_fn,
    targetfield,
    pixel_size=100,
    NoData_value=0,
    extention=(944000, 6503000, 942000, 5414000),
    OutputRasterSRS=3035,
):
    # Open the data source and read in the extent
    source_ds = ogr.Open(vector_fn)
    source_layer = source_ds.GetLayer()
    # The following
    (x_min, x_max, y_min, y_max) = extention
    # Create the destination data source
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)
    driver = gdal.GetDriverByName("GTiff")
    target_ds = driver.Create(
        raster_fn, x_res, y_res, 1, gdal.GDT_Float32, ["compress=LZW"]
    )
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(OutputRasterSRS)
    target_ds.SetProjection(outRasterSRS.ExportToWkt())
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NoData_value)
    # Rasterize
    # Note: the part --> options=["ATTRIBUTE=%s" %targetfield] MUST NOT
    # follow PEP 8. If you change it (with adding space, it won't work.
    gdal.RasterizeLayer(
        target_ds, [1], source_layer, options=["ATTRIBUTE=%s" % targetfield]
    )
    target_ds = None
    source_layer = None
    source_ds = None
    return raster_fn


def specific_demand(inShp, inCSV, outRasterPath, epsg=3035):
    """
    This function reads the input CSV file and save the specific demand values
    into the EU28 shapefile. The obtained shapefile is passed to the rasterize
    function to generate a raster for specific demand values both for
    residential and service sectors.
    """
    temp_dir = os.getcwd() + os.sep + "temp"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    outShapefile = temp_dir + os.sep + "EnergyUseEU28.shp"
    # target fields are fields in CSV that are used to create raster with them
    targetfield = ["Residential", "Service"]
    # dictionary for determination of field types. For easing purposes, integer
    # values are also translated to real values. Do NOT CHANGE IT!
    dict_df = {str: ogr.OFTString, int: ogr.OFTReal, float: ogr.OFTReal}
    # set CRS
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    # Create the output Layer
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    # Remove output shapefile if it already exists
    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    # Create the output shapefile
    outDataSource = outDriver.CreateDataSource(outShapefile)
    outLayer = outDataSource.CreateLayer("Useful_Demand", srs, geom_type=ogr.wkbPolygon)
    # read CSV fields
    df = pd.read_csv(inCSV).values
    # read the headers (first row of each column)
    fieldNames = pd.read_csv(inCSV, nrows=1).columns.values
    # Add fields to the shapefile
    for i, item in enumerate(fieldNames):
        colType = type(df[0, i])
        Field = ogr.FieldDefn(item, dict_df[colType])
        outLayer.CreateField(Field)
    # Get the output Layer's Feature Definition
    outLayerDefn = outLayer.GetLayerDefn()
    # read the input shapefile
    inShapefile = inShp
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(inShapefile, 0)
    inLayer = inDataSource.GetLayer()
    for i in range(0, inLayer.GetFeatureCount()):
        # Get the input Feature
        inFeature = inLayer.GetFeature(i)
        # Create output Feature
        outFeature = ogr.Feature(outLayerDefn)
        temp1 = inFeature.GetField(0)
        # find the row in CSV file which corresponds to the NUTS region
        # obtained from temp1.
        temp2 = np.argwhere(df == temp1)
        if temp2.size > 0:
            for j in range(len(fieldNames)):
                temp = df[temp2[0, 0], j]
                outFeature.SetField(outLayerDefn.GetFieldDefn(j).GetNameRef(), temp)
            geom = inFeature.GetGeometryRef()
            outFeature.SetGeometry(geom)
            # Add new feature to output Layer
            outLayer.CreateFeature(outFeature)
        inFeature = None
        outFeature = None
    # Save and close DataSources
    inDataSource = None
    outDataSource = None
    for field in targetfield:
        name = field
        if len(field) > 10:
            field = field[0:10]
        gdal_rasterize(
            outShapefile,
            outRasterPath + os.sep + "CM19_" + name + "UsefulDemand.tif",
            field,
        )
    shutil.rmtree(temp_dir)
