import json
from os import remove, system
from os.path import exists, isfile

import numpy as np

import gdal
import rasterio
from osgeo import gdal, osr


def get_projection(geofile: str):
    with rasterio.open(geofile) as src_file:
        projection = src_file.crs
    return projection


class RasterNotOverlappedError(Exception):
    """Exception thrown for map size error."""

    pass


def clip_raster(src: str, shapes: dict, dst: str, quiet: bool = True):
    """
    Take a raster and clip it according to polygon defined as a dictionary,
    then save the result.

    Inputs :
        * src : path to the to be clipped raster.
        * shapes : list of dictionaries representing polygons.
        * dst : path where the clipped raster is saved.

    Output :
        * projection : projection of the clipped raster.
    """
    cutline = "cutline.json"
    with open(cutline, "w") as file:
        json.dump(shapes, file)
    command = f"gdalwarp -cutline {cutline} -crop_to_cutline -dstnodata 0 {src} {dst}"
    if quiet:
        command += " -q"
    system(command=command)
    remove(cutline)

    clipped_raster = read_raster(dst, return_geo_transform=False)
    if np.max(clipped_raster) == 0:
        raise RasterNotOverlappedError("Map return is empty.")

    if not isfile(dst):
        raise FileNotFoundError(f"The result file has not been created: {dst}")


def read_raster(raster: str, return_geo_transform=True):
    """
    Open the raster and return the map as a numpy array.

    The geo transform is not return by default.
    The 'return_geo_transform' must be set to True for this.

    See https://gdal.org/tutorials/geotransforms_tut.html,
    for more information about geotransform.

    Inputs :
        * raster :
            - path to the raster.
        * return_geo_transform (optional, set as True by default) :
            - specifying if we want to return the geo transform.
    """

    if exists(raster):
        geofile = gdal.Open(raster)
        if not geofile:
            raise Exception("Unable to load a raster")
    else:
        raise ValueError(f"This path does not refer to existing file : {raster}")

    geo_transform = geofile.GetGeoTransform()
    band = geofile.GetRasterBand(1)
    array = band.ReadAsArray().astype(float)

    geofile = None
    band = None

    if return_geo_transform:
        return array, geo_transform
    else:
        return array


def write_raster(
    map_array: np.array, projection: rasterio.crs.CRS, geotransform: tuple, dst: str
):
    """
    Write a raster based on a map array, projection and geo transform.

    Inputs :
        * map_array: map array.
        * projection: projection of the map array.
        * geotransform: geo transform of the map array.
        * dst: path where the raster is saved.
    """

    if exists(dst):
        remove(dst)
        assert exists(dst) is True, "File not delete"

    # define color bar value
    data_array_scaled = np.interp(
        map_array, (map_array.min(), map_array.max()), (0, 255)
    )

    # Create GeoTIFF
    width = data_array_scaled.shape[1]
    height = data_array_scaled.shape[0]
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(dst, width, height, 1, gdal.GDT_UInt16)

    # Upper Left x, Eeast-West px resolution, rotation, Upper Left y, rotation, North-South px resolution
    dst_ds.SetGeoTransform(geotransform)

    # Set CRS
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(projection.to_epsg())
    dst_ds.SetProjection(srs.ExportToWkt())

    # Write the band
    band = dst_ds.GetRasterBand(1)
    band.WriteArray(array=data_array_scaled)

    # create the color table
    color_table = gdal.ColorTable()
    color_table.CreateColorRamp(
        int(map_array.min()), (112, 153, 89), int(map_array.max()), (214, 193, 156)
    )

    band.SetRasterColorTable(color_table)
    # band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)

    band = None
    dst_ds = None
