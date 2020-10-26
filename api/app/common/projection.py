import gdal
import osr


def proj4_from_geotiff(path):
    raster = gdal.Open(path)
    if not raster:
        return ""
    prj = raster.GetProjection()
    prj = prj.strip()
    if not prj:
        return ""
    srs = osr.SpatialReference(wkt=prj)

    return srs.ExportToProj4()
