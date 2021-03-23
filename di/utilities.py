#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:18:50 2021

@author: giuseppeperonato
"""
import json
import logging
import os

import geopandas as gpd
import pandas as pd
import requests
import sqlalchemy as sqla
from bs4 import BeautifulSoup
from osgeo import gdal, osr


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
            dest_filename = filename + "band" + str(b) + ".tiff"
            print("band", b)
            srcband = ds.GetRasterBand(b)
            if srcband is None:
                continue
            out_ds = gdal.Translate(
                dest_filename, ds, format="GTiff", bandList=[b], outputSRS=srs
            )
            my_dict["time"] = row["time"] + pd.Timedelta(hours=row["dt"]) * (b - 1)
            my_dict["z"] = row["z"]
            my_dict["variable"] = variable
            print(dest_filename)
            my_dict["FID"] = dest_filename
            my_dict["Raster"] = True
            # print(my_dict)
            # print(dicts)
            dicts.append(my_dict)
    # print(dicts)
    data = pd.DataFrame(
        dicts,
        columns=[
            "time",
            "fields",
            "variable",
            "value",
            "ds_id",
            "FID",
            "dt",
            "z",
            "Raster",
        ],
    )
    # data = pd.DataFrame(dicts)
    if delete_orig:
        os.remove(filename)
    return data


def toPostgreSQL(
    data, dbURL="postgresql://postgres:postgres@localhost:5432/dataset", schema="data"
):
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
    logging.info("Loading to PostgreSQL...")
    data.to_sql(schema, db_engine, if_exists="append", index=False)
    logging.info("Done.")


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
    logging.info("Loading to PostGIS...")
    gdf.to_postgis(schema, db_engine, if_exists="append", index=False)
    logging.info("Done.")


def datasetExists(
    ds_id,
    dbURL="postgresql://test:example@localhost:5433/dataset",
    tables=["datasets", "spatial", "data"],
):
    """
    Check whether the datasets exist in all tables.
    Parameters
    ----------
    ds_id : int.
    dbURL : str, optional
        The default is "postgresql://test:example@localhost:5433/dataset".
    tables : list of strings, optional
        The default is ["datasets","spatial","data"].
    Returns
    -------
    bool
    """
    engine = sqla.create_engine(dbURL)
    lengths = []
    for table in tables:
        with engine.connect() as con:
            rs = con.execute(
                "SELECT COUNT(*) FROM {} WHERE ds_id = {}".format(table, ds_id)
            )
            for row in rs:
                count = row[0]
            lengths.append(count)
    if lengths[0] > 0 or lengths[1] > 0 or lengths[2] > 0:
        return True
    else:
        return False


def removeDataset(ds_id, dbURL="postgresql://test:example@localhost:5433/dataset"):
    """
    Delete the dataset.
    Parameters
    ----------
    ds_id : int.
    dbURL : str, optional
        The default is "postgresql://test:example@localhost:5433/dataset".
    Returns
    -------
    None
    """
    engine = sqla.create_engine(dbURL)
    with engine.connect() as con:
        rs = con.execute("DELETE FROM datasets WHERE ds_id = {};".format(ds_id))


def getDataPackage(ds_id, dbURL="postgresql://test:example@localhost:5433/dataset"):
    """
    Retrieve the datapackage.
    Parameters
    ----------
    ds_id : int.
    dbURL : str, optional
        The default is "postgresql://test:example@localhost:5433/dataset".
    Returns
    -------
    datatpackage: json string.
    """
    engine = sqla.create_engine(dbURL)
    df = pd.read_sql(
        "SELECT * FROM datasets WHERE ds_id = {};".format(ds_id), con=engine
    )
    if len(df) > 0:
        metadata = df.loc[0, "metadata"]
        return metadata.get("datapackage")
    else:
        return None


def get_ld_json(url: str) -> dict:
    """Parse JSON-LD. Source: https://stackoverflow.com/a/59113576."""
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    return json.loads(
        "".join(soup.find("script", {"type": "application/ld+json"}).contents)
    )
