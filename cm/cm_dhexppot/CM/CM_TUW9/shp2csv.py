# -*- coding: utf-8 -*-
"""
Created on July 6 2017

@author: fallahnejad@eeg.tuwien.ac.at
"""
import os
import sys
import time

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
"""
- The user can select a region which is potentially larger than his/her
uploaded layer. An upper hand module should combine the uploaded layer with the
default building layer and submit a shapefile covering the "selected region by
user" to this module.
- This code expects that the default layer provides information regarding
number of floors as well.
- The demand of each building, if applicable, should be entered in kWh.
- Column "Type" should be either "0" for residential or "1" for service sector
- if the user no Type field for his/her own shapefile provides, all buildings
within his/her shapefile will be considered as residential. For the regions
coming from OSM, the OSM usage will be attributed to the Type.
- OSM building usage is also expected to be input as 0 and 1.
- The output CSV file only includes the data which are relevant for the BUHDM.
###############################################################################
Explanation of indexing in this code:
shape fields: [a  b  c  d  e  f  g  h  i  j]
fieldList :   [j  f  i  d]
fIndex:       [9 -1  5  8  -1 3 -1 -1 -1 -1]
newFieldList  [0  2  3  5]
###############################################################################
Units of input/output data:
    GFA: [m2]
    demand: [kWh/a]
    spec_demand: [kWh/m2]
"""


def indexing(UsefulDemandRaster, X, Y):
    UsefulDemandDataSource = gdal.Open(UsefulDemandRaster)
    transform = UsefulDemandDataSource.GetGeoTransform()
    x0 = transform[0]
    y0 = transform[3]
    resolution = transform[1]
    xIndex = np.floor((X - x0) / resolution).astype(int)
    yIndex = np.floor((y0 - Y) / resolution).astype(int)
    band1 = UsefulDemandDataSource.GetRasterBand(1)
    arrUsefulDemand = band1.ReadAsArray()
    # find the indices which are out of range of the raster
    h, w = arrUsefulDemand.shape
    l = yIndex.size
    # define specific demand array with the same length as l and fill it with
    # NaN
    spec_demand = np.empty(l)
    outRangeY = np.concatenate(
        (np.argwhere(yIndex < 0), np.argwhere(yIndex >= h)), axis=0
    )
    outRangeX = np.concatenate(
        (np.argwhere(xIndex < 0), np.argwhere(xIndex >= w)), axis=0
    )
    outRange = np.union1d(outRangeY, outRangeX)
    IndexInRange = np.setdiff1d(np.arange(l), outRange)
    # fill elements which are in range
    spec_demand[IndexInRange] = arrUsefulDemand[
        yIndex[IndexInRange], xIndex[IndexInRange]
    ]
    UsefulDemandDataSource = None
    return spec_demand


def shp2csv(inShapefile, UsefulDemandRaster, outCSV, epsg=3035):
    # Get the input layer
    driver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSet = driver.Open(inShapefile)
    inLayer = inDataSet.GetLayer()
    # Get projection from input Layer
    inSpatialRef = inLayer.GetSpatialRef()
    # Desired projection is EPSG3035
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(epsg)
    # Compare projection of input layer and the desired projection and
    # create the coordinate transformation parameter
    flag = False
    if inSpatialRef != outSpatialRef:
        flag = True
        coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    inLayerDefn = inLayer.GetLayerDefn()
    feat_count = inLayer.GetFeatureCount()
    # List of the fields which are expected to be seen in the input layer.
    # update the comment in "update_building_layer" regarding input csv
    fieldList = np.array(
        [
            "hotmaps_ID",
            "inputLyr_ID",
            "Type",
            "Year_Construction",
            "Address",
            "Footprint",
            "NrFloor",
            "GFA",
            "spec_demand",
            "demand",
            "X_3035",
            "Y_3035",
        ],
        dtype=str,
    )
    fieldListSize = fieldList.size
    # Determine the location of parameters in the above field list
    demIndex = int(np.argwhere(fieldList == "demand"))
    typIndex = int(np.argwhere(fieldList == "Type"))
    xIndex = int(np.argwhere(fieldList == "X_3035"))
    yIndex = int(np.argwhere(fieldList == "Y_3035"))
    FootprintIndex = int(np.argwhere(fieldList == "Footprint"))
    NrFloorIndex = int(np.argwhere(fieldList == "NrFloor"))
    GFAIndex = int(np.argwhere(fieldList == "GFA"))
    spec_demandIndex = int(np.argwhere(fieldList == "spec_demand"))
    # Initialize the field values with "NaN". This is important to distinguish
    # between 0 and unavailable data
    fieldvalues = np.nan * np.empty((feat_count, fieldListSize))
    fieldvalues[:, typIndex] = 0
    usefulDemand = np.zeros((feat_count, len(UsefulDemandRaster)))
    # 1 is assigned to Nr. of floors. If no data for that would be available,
    # only the net floor area will be considered for the calculation.
    fieldvalues[:, NrFloorIndex] = 1
    # Attribute -1 to all field indices and update them if they exist in the
    # input layer.
    fIndex = -1 * np.ones(fieldListSize)
    for i in range(inLayerDefn.GetFieldCount()):
        temp1 = inLayerDefn.GetFieldDefn(i).GetName()
        if temp1 in fieldList:
            fIndex[np.argwhere(fieldList == temp1)] = i
    # Update the field list with those which also exist in the input layer
    newFieldList = np.argwhere(fIndex != -1)
    # loop through the input features
    inFeature = inLayer.GetNextFeature()
    while inFeature:
        fid = inFeature.GetFID()
        fieldvalues[fid, 0] = fid
        # get the input geometry
        geom = inFeature.GetGeometryRef()
        if flag:
            # change projection of the geometry
            geom.Transform(coordTrans)
        fieldvalues[fid, xIndex] = geom.Centroid().GetX()
        fieldvalues[fid, yIndex] = geom.Centroid().GetY()
        for item in newFieldList:
            fieldvalues[fid, item] = inFeature.GetField(int(fIndex[item]))
        """
        Footprint should be assigned after above for-loop in order to prevent
        overwriting of Footprint corresponding to those attributes that coming
        from OSM and not from user inputs --> case large selected area with
        small input data provided by user.
        Footprint may exist in the input shapefile for some attributes;
        however, recalculation of it does not cause deviation since basically
        it is should be similar to the input
        """
        if geom.GetGeometryName() == "POINT":
            fieldvalues[fid, FootprintIndex] = 0
        else:
            fieldvalues[fid, FootprintIndex] = geom.GetArea()
        inFeature = inLayer.GetNextFeature()
    if "GFA" not in fieldList[newFieldList]:
        fieldvalues[:, GFAIndex] = (
            fieldvalues[:, FootprintIndex] * fieldvalues[:, NrFloorIndex]
        )
    else:
        # Assign a value to GFA for the attributes that have no entries
        k = np.argwhere(
            np.isnan(fieldvalues[:, GFAIndex]) + fieldvalues[:, GFAIndex] == 0
        )
        noGFA = k[::2]
        fieldvalues[noGFA, GFAIndex] = (
            fieldvalues[noGFA, FootprintIndex] * fieldvalues[noGFA, NrFloorIndex]
        )
    for i, raster in enumerate(UsefulDemandRaster):
        usefulDemand[:, i] = indexing(
            raster, fieldvalues[:, xIndex], fieldvalues[:, yIndex]
        )
    if "demand" not in fieldList[newFieldList]:
        if "spec_demand" not in fieldList[newFieldList]:
            if "Type" not in fieldList[newFieldList]:
                fieldvalues[:, spec_demandIndex] = usefulDemand[:, 0]
            else:
                """
                it is possible that some attributes have no value for Type
                (unknown buildings). The assumption is that all unknown
                buildings will be considered as residential building. So, in
                query for residential attributes, "!= 1" is used.
                """
                res = np.argwhere(fieldvalues[:, typIndex] != 1)
                serv = np.argwhere(fieldvalues[:, typIndex] == 1)
                fieldvalues[res, spec_demandIndex] = usefulDemand[res, 0]
                fieldvalues[serv, spec_demandIndex] = usefulDemand[serv, 1]
        spec_demand = fieldvalues[:, spec_demandIndex]
        GFA = fieldvalues[:, GFAIndex]
        fieldvalues[:, demIndex] = spec_demand * GFA
    """
    this part of the code is implemented to cover the situation in which user
    has selected a region and within a smaller part of that region, he has
    provided a set of data. Therefore, the entries coming from OSM, do not
    have demand data. in this case, the standard country demand value will be
    attributed.
    """
    k = np.argwhere(np.isnan(fieldvalues[:, demIndex]))
    if k:
        noDemandRows = k[::2]
        res = np.argwhere(fieldvalues[noDemandRows, typIndex] != 1)
        serv = np.argwhere(fieldvalues[noDemandRows, typIndex] == 1)
        fieldvalues[res, spec_demandIndex] = usefulDemand[res, 0]
        fieldvalues[serv, spec_demandIndex] = usefulDemand[serv, 1]
        GFA_noData = fieldvalues[noDemandRows, GFAIndex]
        spec_demand_noData = fieldvalues[noDemandRows, spec_demandIndex]
        fieldvalues[noDemandRows, demIndex] = spec_demand_noData * GFA_noData
    df = pd.DataFrame(fieldvalues, columns=fieldList, index=np.arange(feat_count))
    df = df[fieldList]
    df = df.sort_values(["hotmaps_ID"])
    df.to_csv(outCSV)
    inDataSet = None
    df = None
