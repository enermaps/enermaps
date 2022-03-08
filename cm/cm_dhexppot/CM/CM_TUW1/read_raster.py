from osgeo import gdal


def raster_array(
    raster, dType=float, xOff=None, yOff=None, cols=None, rows=None, return_gt=None
):
    ds = gdal.Open(raster)
    if not ds:
        raise Exception(" unable to load a raster")
    geo_transform = ds.GetGeoTransform()
    gt = list(geo_transform)
    if xOff:
        xOffset = int((xOff - geo_transform[0]) / geo_transform[1])
        gt[0] = xOff
    else:
        xOffset = 0
    if yOff:
        yOffset = int((yOff - geo_transform[3]) / geo_transform[5])
        gt[3] = yOff
    else:
        yOffset = 0
    band1 = ds.GetRasterBand(1)
    arr = band1.ReadAsArray(xOffset, yOffset, cols, rows).astype(dType)
    ds = None
    if return_gt:
        return arr, tuple(gt)
    else:
        return arr
