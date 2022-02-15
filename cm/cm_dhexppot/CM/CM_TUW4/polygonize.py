import numpy as np
import os
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import sys
from scipy.ndimage import measurements
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW1.read_raster import raster_array as RA




def rgba(minimum, maximum, value, a=0.5):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    output = "(" + str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a) + ")"
    return output


def add_label_field(dh_bool_raster, label_raster, output_shp1, output_shp2,
                    heat_dem_coh, epsg=3035):
    label_list = []
    color_map = ["#feedde", "#fdd0a2", "#fdae6b", "#fd8d3c",
                 "#e6550d", "#a63603"]
    min_val_dh, max_val_dh = np.min(heat_dem_coh) , np.max(heat_dem_coh)
    diff = max_val_dh - min_val_dh
    # calculate the teps in legend. 6 steps are generated
    if diff > 0:
        if min_val_dh > diff/4:
            symbol_vals = [round(min_val_dh - diff/8 + i*diff/4, 1) for i in range(5)]
        else:
            symbol_vals = [round(min_val_dh + i*diff/4, 1) for i in range(5)]
    else:
        # synthesis_diff of 1 GWh
        synthesis_diff = 1
        symbol_vals = [round(min_val_dh - 1 + i*synthesis_diff/2, 1) for i in range(5)]
    symbol_vals_str = [str(item) for item in symbol_vals]
    '''
    check each value of demands falls into which category of the legend
    if symbol_vals = [a, b, c, d, e], the classes are
        x < a         class 0
        a <= x < b    class 1
        b <= x < c    class 2
        ...
        f <= x        class 5
    - values bellow smallest element in symbol_vals get 0
    - values above largest element in symbol_vals get 5
    '''
    dem_legend_index = np.searchsorted(symbol_vals, heat_dem_coh, side='right')
    
    
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    # Remove output shapefile if it already exists
    if os.path.exists(output_shp2):
        outDriver.DeleteDataSource(output_shp2)
    bool_arr, gt = RA(dh_bool_raster, return_gt=True)
    label_arr = RA(label_raster)
    numLabels = np.max(label_arr)
    coords = measurements.center_of_mass(bool_arr, label_arr,
                                         index=np.arange(1, numLabels+1))
    x0, y0, w, h = gt[0], gt[3], gt[1], gt[5]
    X0 = x0 + w/2
    Y0 = y0 + h/2
    for item in coords:
        xl = round(X0 + 100 * item[1], 1)
        yl = round(Y0 - 100 * item[0], 1)
        label_list.append((xl, yl))
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(output_shp1, 0)
    inLayer = inDataSource.GetLayer()
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    geom_typ = inLayer.GetGeomType()
    geom_typ_dict = {1: ogr.wkbPoint, 2: ogr.wkbLineString, 3: ogr.wkbPolygon}
    # Create the output Layer
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    outDataSource = outDriver.CreateDataSource(output_shp2)
    outLayer = outDataSource.CreateLayer("newSHP", srs,
                                         geom_type=geom_typ_dict[geom_typ])
    Fields = ['Label', 'Dem_DhArea', 'color', 'fillColor', 'opacity']
    Fields_dtype = [ogr.OFTInteger, ogr.OFTString, ogr.OFTString,
                    ogr.OFTString, ogr.OFTString]
    for i, f in enumerate(Fields):
        Field = ogr.FieldDefn(f, Fields_dtype[i])
        outLayer.CreateField(Field)
    # Get the output Layer's Feature Definition
    outLayerDefn = outLayer.GetLayerDefn()
    for feature in inLayer:
        geom = feature.GetGeometryRef()
        centroid = geom.Centroid()
        x = round(centroid.GetX(), 1)
        y = round(centroid.GetY(), 1)
        outFeature = ogr.Feature(outLayerDefn)
        try:
            geom_label = label_list.index((x, y))
        except:
            nearest_dist = 1000
            for p, point in enumerate(label_list):
                x_temp, y_temp = point
                temp_dist = ((x-x_temp)**2 + (y-y_temp)**2)**0.5
                if temp_dist < nearest_dist:
                    geom_label = p
        outFeature.SetField(outLayerDefn.GetFieldDefn(0).GetNameRef(),
                            geom_label+1)
        try:
            outFeature.SetField(outLayerDefn.GetFieldDefn(1).GetNameRef(),
                                str(round(heat_dem_coh[geom_label], 2)) + " GWh")
            outFeature.SetField(outLayerDefn.GetFieldDefn(2).GetNameRef(),
                                color_map[dem_legend_index[geom_label]])
            outFeature.SetField(outLayerDefn.GetFieldDefn(3).GetNameRef(),
                                color_map[dem_legend_index[geom_label]])
            outFeature.SetField(outLayerDefn.GetFieldDefn(4).GetNameRef(),
                                "0.5")
        except:
            outFeature.SetField(outLayerDefn.GetFieldDefn(1).GetNameRef(),
                                "-")
            outFeature.SetField(outLayerDefn.GetFieldDefn(2).GetNameRef(),
                                "-")
            outFeature.SetField(outLayerDefn.GetFieldDefn(3).GetNameRef(),
                                "-")
            outFeature.SetField(outLayerDefn.GetFieldDefn(4).GetNameRef(),
                                "-")
        outFeature.SetGeometry(geom)
        # Add new feature to output Layer
        outLayer.CreateFeature(outFeature)
        outFeature = None
    # Save and close DataSources
    inDataSource = None
    outDataSource = None
    if os.path.exists(output_shp1):
        outDriver.DeleteDataSource(output_shp1)
    return symbol_vals_str


def polygonize(dh_bool_raster, label_arr, output_shp1, output_shp2,
               heat_dem_coh, epsg=3035):
    # save the coherent areas in shapefile format
    raster = gdal.Open(dh_bool_raster)
    band = raster.GetRasterBand(1)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    shpDriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(output_shp1):
        shpDriver.DeleteDataSource(output_shp1)
    outDataSource = shpDriver.CreateDataSource(output_shp1)
    outLayer = outDataSource.CreateLayer('outPolygon', srs,
                                         geom_type=ogr.wkbPolygon)
    newField = ogr.FieldDefn('FID', ogr.OFTInteger)
    outLayer.CreateField(newField)
    # polygonize
    gdal.Polygonize(band, band, outLayer, 0, options=["8CONNECTED=8"])
    # save layer
    outDataSource = outLayer = band = None
    symbol_vals_str = add_label_field(dh_bool_raster, label_arr, output_shp1,
                                      output_shp2, heat_dem_coh)
    return symbol_vals_str
