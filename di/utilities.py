#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:18:50 2021

@author: giuseppeperonato
"""
from osgeo import gdal, osr
import pandas as pd
import geopandas as gpd
import os
import sqlalchemy as sqla

def prepareRaster(df, srs="EPSG:3035", variable="", delete_orig=False):
    """
    Convert original raster or NetCDF into EnerMaps rasters (single band, GeoTiff, EPSG:3035)

    Parameters
    ----------
    df : DataFrame.
        Results of API extraction.

    Returns
    -------
    df : DataFrame
        Results with schema for EnerMaps data table

    """
    dicts = []
    for i, row in df.iterrows():
        filename = row["value"]
        if filename[-2:] == "nc":
            src_ds = gdal.Open("NETCDF:{0}:{1}".format(filename, variable))
        else:
            src_ds = gdal.Open(filename)
        source_wkt = src_ds.GetProjectionRef()
        dest_wkt = osr.SpatialReference()
        dest_wkt.ImportFromEPSG(int(srs.split(":")[-1])) 
        dest_wkt = dest_wkt.ExportToPrettyWkt()
        
        ds = gdal.AutoCreateWarpedVRT(src_ds, source_wkt, dest_wkt)
        for b in range(ds.RasterCount):
            my_dict = {}
            b += 1
            dest_filename = filename + 'band' + str(b) + '.tiff'
            print("band", b)
            srcband = ds.GetRasterBand(b)
            if srcband is None:
                continue
            out_ds = gdal.Translate(dest_filename,
                                    ds, format='GTiff',
                                    bandList=[b],
                                    outputSRS=srs)
            my_dict["time"] = row["time"] + pd.Timedelta(hours=row["dt"])*(b-1)
            my_dict["z"] = row["z"]
            my_dict["variable"] = variable
            print(dest_filename)
            my_dict["FID"] = dest_filename
            my_dict["Raster"] = True
            # print(my_dict)
            # print(dicts)
            dicts.append(my_dict)
    # print(dicts)
    data = pd.DataFrame(dicts, columns=["time","fields","variable","value","ds_id","FID", "dt","z","Raster"])
    # data = pd.DataFrame(dicts)
    if delete_orig:
        os.remove(filename)
    return data


def toPostgreSQL(data, dbURL="postgresql://postgres:postgres@localhost:5432/dataset", schema="data"):
    """
    Load admin_units to pgsql.

    Parameters
    ----------
    rasterdf : GeoDataFrame
        Table with all rasters to be loaded
    dbURL : string, optional
        SQLAlchemy database URL. The default is 'postgresql://postgres:postgres@localhost:5432/dataset'.

    Returns
    -------
    None.

    """
    db_engine = sqla.create_engine(dbURL)
    print("Loading raster to PostgreSQL...")
    data.to_sql(schema, db_engine, if_exists="append", index=False)
    print("Done.")
    
def toPostGIS(
    gdf, dbURL="postgresql://postgres:postgres@localhost:5432/dataset", schema="spatial"
):
    """
    Load admin_units to pgsql.

    Parameters
    ----------
    admin_units : GeoDataFrame
        Table with all administrative units..
    dbURL : string, optional
        SQLAlchemy database URL. The default is 'postgresql://postgres:postgres@localhost:5432/dataset'.

    Returns
    -------
    None.

    """
    db_engine = sqla.create_engine(dbURL)
    print("Loading to PostGIS...")
    gdf.to_postgis(schema, db_engine, if_exists="append", index=False)
    print("Done.")