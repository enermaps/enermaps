# -*- coding: utf-8 -*-
"""
Created on July 6 2017

@author: fallahnejad@eeg.tuwien.ac.at
"""
import os
import sys
import time

import pandas as pd
from osgeo import ogr, osr

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
"""
This module creates a shapefile with attributes which exist in the input
shapefile of shp2csv.py module and assigns the calculated values to the
features of this shapefile.
"""


def update_building_lyr(inputCSV, inShapefile, outShapefile, epsg=3035):
    # fields in CSV are as follows:
    # ['hotmaps_ID', 'inputLyr_ID', 'Type', 'Year_Construction', 'Address',
    # 'Footprint', 'NrFloor', 'GFA', 'spec_demand', 'demand', 'X_3035',
    # 'Y_3035']
    ifile = pd.read_csv(inputCSV)
    ifile = ifile.sort_values(["hotmaps_ID"])
    csv_cols = ifile.columns.values
    col_dtype = ifile.dtypes.values
    # Get the input layer
    driver = ogr.GetDriverByName("ESRI Shapefile")

    inDataSource = driver.Open(inShapefile)
    inLayer = inDataSource.GetLayer()
    # set CRS
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)
    # Create the output shapefile
    outDataSource = outDriver.CreateDataSource(outShapefile)
    geom_typ = inLayer.GetGeomType()
    geom_typ_dict = {1: ogr.wkbPoint, 2: ogr.wkbLineString, 3: ogr.wkbPolygon}
    if geom_typ not in list(geom_typ_dict.keys()):
        raise Exception("Geometry type of the input layer is not supported!")
    outLayer = outDataSource.CreateLayer(
        "Building_lyr_updated", srs, geom_type=geom_typ_dict[geom_typ]
    )
    for i, item in enumerate(csv_cols):
        # shapefile's field name should not exceed 10 characters. O.W. warning
        # will be printed. To avoid waning, the following is applied:
        item = item[:10]
        if i > 0:
            if col_dtype[i] == object:
                Field = ogr.FieldDefn(item, ogr.OFTString)
            elif col_dtype[i] == int:
                Field = ogr.FieldDefn(item, ogr.OFTInteger)
            else:
                Field = ogr.FieldDefn(item, ogr.OFTReal)
            outLayer.CreateField(Field)
    outLayerDefn = outLayer.GetLayerDefn()
    # loop through the input features
    inFeature = inLayer.GetNextFeature()
    while inFeature:
        fid = inFeature.GetFID()
        outFeature = ogr.Feature(outLayerDefn)
        # get the input geometry
        for i, item in enumerate(csv_cols):
            if i > 0:
                outFeature.SetField(
                    outLayerDefn.GetFieldDefn(i - 1).GetNameRef(),
                    (ifile[item].values)[fid],
                )
        geom = inFeature.GetGeometryRef()
        outFeature.SetGeometry(geom)
        outLayer.CreateFeature(outFeature)
        outFeature = None
        inFeature = inLayer.GetNextFeature()
        # Save and close DataSources
    inDataSource = None
    outDataSource = None
