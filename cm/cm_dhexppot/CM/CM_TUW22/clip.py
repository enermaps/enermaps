import os
import sys

import numpy as np
import pandas as pd

# from docutils.io import InputError
from osgeo import gdalnumeric, ogr
from PIL import Image, ImageDraw

import CM.CM_TUW19.run_cm as CM19
import CM.CM_TUW21.run_cm as CM21

# import pdb
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def saveCSVorSHP(
    feat,
    demand,
    features_path,
    output_dir,
    prefix="",
    save2csv=None,
    save2shp=None,
    OutputSRS=3035,
):
    df = pd.DataFrame()
    df["id"] = np.array(feat)
    df["Sum"] = np.array(demand)
    csv_path = output_dir + os.sep + prefix + "_clip_result.csv"
    outShpPath = output_dir + os.sep + prefix + "_clip_result.shp"
    new_csv_path = csv_path
    new_outShpPath = outShpPath
    i = 1
    while os.path.exists(new_csv_path):
        new_csv_path = csv_path[:-4] + " (" + str(i) + ").csv"
        i = i + 1
    i = 1
    while os.path.exists(new_outShpPath):
        new_outShpPath = outShpPath[:-4] + " (" + str(i) + ").shp"
        i = i + 1
    if save2csv:
        df.to_csv(new_csv_path)
    if save2shp:
        CM21.main(features_path, df, new_outShpPath, OutputSRS=OutputSRS)


def clip_raster(
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
    suffix_namefield=None,
    add_suffix=None,
):
    """
    Clips a raster (given a numpy.array and its geo-transform array) to a
    polygon layer provided by a Shapefile (or other vector layer). Returns an
    array. Clip features can be multi-part geometry and with interior ring
    inside them.

    The code supports most of raster and clip vector arrangements; however,
    it does not support cases in which clip vector extent (envlope of it) goes
    beyond more than 2 sides of the raster.

    Arguments:
        rast               A NumPy array
        features_path      The path to the clipping layer
        gt                 GDAL GeoTransform array
        nodata             The NoData value; defaults to -9999
        save2csv           should the outputs be saved in a csv file as well?
        unit_multiplier    Factor to be multiplied into the summation to
                           output the desired unit.
        suffix_namefield   What to add at the end of the file name. must be field of shape file
    """

    def image_to_array(i):
        """
        Converts a Python Imaging Library (PIL) array to a gdalnumeric image.
        """
        a = gdalnumeric.fromstring(i.tobytes(), "b")
        a.shape = i.im.size[1], i.im.size[0]
        return a

    def world_to_pixel(geo_matrix, x, y):
        """
        Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
        the pixel location of a geospatial coordinate;
        """
        ulX = geo_matrix[0]
        ulY = geo_matrix[3]
        xDist = geo_matrix[1]
        yDist = geo_matrix[5]
        rtnX = geo_matrix[2]
        rtnY = geo_matrix[4]
        pixel = int((x - ulX) / xDist)
        line = int((ulY - y) / xDist)
        return (pixel, line)

    clip_complete = None
    # get shapefile name
    shpName = features_path.replace("\\", "/")
    shpName = shpName.split("/")[-1][0:-4]
    # Create a data array for the output csv
    if save2csv:
        feat = []
        demand = []
    if unit_multiplier is None:
        unit_multiplier = 1.0
    xRes, yRes = rast.shape
    # Create an OGR layer from a boundary shapefile
    features = ogr.Open(features_path)
    if features.GetDriver().GetName() == "ESRI Shapefile":
        temp = os.path.split(os.path.splitext(features_path)[0])
        lyr = features.GetLayer(temp[1])
    else:
        lyr = features.GetLayer()
    for fid in range(lyr.GetFeatureCount()):
        flag = np.zeros(4)
        """
        if fid > 40:
            continue
        """
        poly = lyr.GetFeature(fid)
        fname = poly.GetField("CNTR_ID")
        geom = poly.GetGeometryRef()
        if suffix_namefield is not None:
            suffix = poly.GetField(suffix_namefield)
            if add_suffix is not None:
                suffix = "_" + add_suffix + "_" + suffix
        else:
            suffix = "feature_" + str(fid)
        # Convert the feature extent to image pixel coordinates
        minX, maxX, minY, maxY = geom.GetEnvelope()
        ulX, ulY = world_to_pixel(gt, minX, maxY)
        lrX, lrY = world_to_pixel(gt, maxX, minY)
        # Calculate the pixel size of the new image
        pxWidth = int(lrX - ulX)
        pxHeight = int(lrY - ulY)
        # If the clipping features extend out-of-bounds and ABOVE the raster...
        if gt[3] < maxY:
            if gt[3] < minY:
                continue
            else:
                # In such a case. ulY ends up being negative--can't have that!
                ulY = 0
                flag[0] = 1
        if gt[0] > minX:
            if gt[0] > maxX:
                continue
            else:
                ulX = 0
                flag[1] = 1
        rastXmax = gt[0] + yRes * gt[1]
        if rastXmax < maxX:
            if rastXmax < minX:
                continue
            else:
                lrX = yRes
                flag[2] = 1
        rastYmin = gt[3] + xRes * gt[5]
        if rastYmin > minY:
            if rastYmin > maxY:
                continue
            else:
                lrY = xRes
                flag[3] = 1
        flag_sum = np.sum(flag)
        # Multi-band image?
        try:
            clip = rast[:, ulY:lrY, ulX:lrX]
        except IndexError:
            clip = rast[ulY:lrY, ulX:lrX]
        geometry_counts = geom.GetGeometryCount()
        clip_complete = np.zeros((pxHeight, pxWidth), clip.dtype)
        # perform the process for multi-part features
        for i in range(geometry_counts):
            # Do not delete this. Clip is set to None in each iteration and
            # should be initialized here again.
            try:
                clip = rast[:, ulY:lrY, ulX:lrX]
            except IndexError:
                clip = rast[ulY:lrY, ulX:lrX]
            # Create a new geomatrix for the image
            gt2 = list(gt)
            gt2[0] = gt2[1] * int(minX / gt2[1])
            gt2[3] = gt2[1] * int(maxY / gt2[1])
            if gt2[3] < maxY:
                gt2[3] = gt2[1] * int(maxY / gt2[1] + 1)
            # Map points to pixels for drawing the boundary on a blank 8-bit,
            # black and white, mask image.
            points = []
            pixels = []
            # check multi-part geometries
            if geometry_counts > 1:
                geom1 = geom.GetGeometryRef(i)
                # check multi-part geometry with interior ring
                if geom1.GetGeometryName() == "LINEARRING":
                    pts = geom1
                else:
                    # get outer ring of polygon
                    pts = geom1.GetGeometryRef(0)
                # print(geom1.GetGeometryName() + ' ' + pts.GetGeometryName())
            else:
                # get outer ring of polygon
                pts = geom.GetGeometryRef(0)
            for p in range(pts.GetPointCount()):
                points.append((pts.GetX(p), pts.GetY(p)))
            for p in points:
                pixels.append(world_to_pixel(gt2, p[0], p[1]))
            raster_poly = Image.new("L", (pxWidth, pxHeight), 1)
            rasterize = ImageDraw.Draw(raster_poly)
            # Fill with zeroes
            rasterize.polygon(pixels, 0)
            premask = image_to_array(raster_poly)
            # with the calculated geotransform matrix gt2, clip matrix should
            # have the same dimension as premask
            clip_new = np.zeros_like(premask, clip.dtype)
            if flag_sum == 0:
                mask = premask
                clip_new = gdalnumeric.choose(mask, (clip, nodata))
            else:
                if flag_sum < 3:
                    row_clip, col_clip = clip.shape
                    index = np.array(
                        [
                            -flag[0] * row_clip,
                            flag[3] * row_clip,
                            -flag[1] * col_clip,
                            flag[2] * col_clip,
                        ]
                    ).astype(int)
                    mask_index = np.where(index == 0, None, index)
                    mask = premask[
                        mask_index[0] : mask_index[1], mask_index[2] : mask_index[3]
                    ]
                    clip = gdalnumeric.choose(mask, (clip, nodata))
                    clip_new[
                        mask_index[0] : mask_index[1], mask_index[2] : mask_index[3]
                    ] = clip
                else:
                    s = 1
            #                    raise InputError('Clip for the feature %d is not '
            #                                     'supported' % fid)
            m1, n1 = np.nonzero(clip_new)
            clip_stack = set(list(zip(m1, n1)))
            m2, n2 = np.nonzero(clip_complete)
            clip_complete_stack = set(list(zip(m2, n2)))
            intersect_clip = clip_complete_stack.intersection(clip_stack)
            if len(intersect_clip) == 0:
                clip_complete = clip_complete + clip_new
            else:
                clip_complete = clip_complete - clip_new
            mask = None
            premask = None
            raster_poly = None
            rasterize = None
            geom1 = None
            pts = None
            gt3 = gt2
            gt2 = None
            clip = None
            clip_new = None
        if save2csv:
            nuts_region = str(poly.GetField(0))
            dem_sum = np.sum(clip_complete) * unit_multiplier
            if dem_sum > 0:
                feat.append(nuts_region)
                demand.append(dem_sum)
                print(
                    "The sum of values within the region %s is: %0.1f"
                    % (nuts_region, dem_sum)
                )
        if save2raster:
            if not save2csv:
                dem_sum = np.sum(clip_complete) * unit_multiplier
            if dem_sum > 0:
                outRasterPath = output_dir + os.sep + fname + "_" + str(fid) + ".tif"
                CM19.main(
                    outRasterPath, gt3, str(clip_complete.dtype), clip_complete, 0
                )
    if save2csv or save2shp:
        saveCSVorSHP(
            feat,
            demand,
            features_path,
            output_dir,
            shpName,
            save2csv,
            save2shp,
            OutputSRS=OutputSRS,
        )
    if return_array:
        return clip_complete, gt3
