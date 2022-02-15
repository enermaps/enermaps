import os
import sys
import time
import numpy as np
from osgeo import ogr
from osgeo import osr
import pandas as pd
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
'''
inputs:
    inShpPath:    path to the input shp file
    inCSV:        path to the input csv file or Pandas DataFrame
    outShpPath:   path for saving the output shp
    OutputSRS:    crs that will be used for the output shapefile
'''


def csv2shapefile(inShpPath, inCSV, outShpPath, id_field='id', shp_id_field=0,
                  OutputSRS=3035):
    # read the input shapefile
    inShapefile = inShpPath
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(inShapefile, 0)
    inLayer = inDataSource.GetLayer()
    # set CRS
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(OutputSRS)
    # Create the output Layer
    outShapefile = outShpPath
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    # Remove output shapefile if it already exists
    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    # Create the output shapefile
    outDataSource = outDriver.CreateDataSource(outShapefile)
    geom_typ = inLayer.GetGeomType()
    geom_typ_dict = {1: ogr.wkbPoint, 2: ogr.wkbLineString, 3: ogr.wkbPolygon}
    outLayer = outDataSource.CreateLayer("outLyr", srs,
                                         geom_type=geom_typ_dict[geom_typ])
    if isinstance(inCSV, str):
        # read CSV file
        ifile = pd.read_csv(inCSV)
    else:
        ifile = inCSV
    df = ifile.values
    ID = ifile[id_field].astype(str)
    check_null = ifile.notnull().values
    # read the headers (first row of each column)
    fieldNames = ifile.columns.values
    '''
    ogr field types definition:
    OFTInteger=0, OFTIntegerList=1, OFTReal=2, OFTRealList=3,
    OFTString=4, OFTStringList=5, OFTWideString=6, OFTWideStringList=7,
    OFTBinary=8, OFTDate=9, OFTTime=10, OFTDateTime=11,
    OFTInteger64=12, OFTInteger64List=13, OFTMaxType=13
    '''
    dict_ogr_dtypes = {np.dtype('O'): 4,
                       np.dtype('int64'): 12,
                       np.dtype('float64'): 2}
    for i, item in enumerate(fieldNames):
        # if key does not exist, the column will be considered as string
        Field = ogr.FieldDefn(fieldNames[i],
                              dict_ogr_dtypes.get(ifile[item].dtypes, 4))
        outLayer.CreateField(Field)
    # Get the output Layer's Feature Definition
    outLayerDefn = outLayer.GetLayerDefn()
    for i in range(0, inLayer.GetFeatureCount()):
        # Get the input Feature
        inFeature = inLayer.GetFeature(i)
        # Create output Feature
        outFeature = ogr.Feature(outLayerDefn)
        temp1 = inFeature.GetField(shp_id_field)
        # find the row in CSV file which corresponds to the NUTS region
        # obtained from temp1.
        temp2 = np.argwhere(ID == str(temp1))
        for j in range(len(fieldNames)):
            temp0 = check_null[temp2, j]
            if temp0:
                temp = df[temp2, j][0][0]
                outFeature.SetField(outLayerDefn.GetFieldDefn(j).GetNameRef(),
                                    temp)
        geom = inFeature.GetGeometryRef()
        outFeature.SetGeometry(geom)
        # Add new feature to output Layer
        outLayer.CreateFeature(outFeature)
        inFeature = None
        outFeature = None
    # Save and close DataSources
    inDataSource = None
    outDataSource = None

if __name__ == "__main__":
    start = time.time()
    # path to the src
    data_warehouse = path + os.sep + 'AD/data_warehouse'
    inShpPath = data_warehouse + os.sep + "AT_NUTS3.shp"
    inCSV = data_warehouse + os.sep + "CM.TUW.22.csv2shp.csv"
    output_dir = path + os.sep + 'Outputs'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    outShpPath = output_dir + os.sep + "CM_TUW22_csv2shp.shp"
    csv2shapefile(inShpPath, inCSV, outShpPath)
    elapsed = time.time() - start
    print("%0.3f seconds" % elapsed)
