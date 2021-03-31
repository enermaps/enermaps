#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:18:50 2021

@author: giuseppeperonato
"""
import json
import logging
import os
from pathlib import Path

import geopandas as gpd
import pandas as pd
import psycopg2 as ps
import requests
import sqlalchemy as sqla
from bs4 import BeautifulSoup
from osgeo import gdal, osr
from psycopg2 import sql
from pyproj import CRS


def prepareRaster(
    df: pd.DataFrame,
    crs: CRS = CRS.from_epsg(3035),
    variable: str = "",
    delete_orig: bool = False,
):
    """
    Convert original raster or NetCDF into EnerMaps rasters (single band, GeoTiff, EPSG:3035).

    Parameters
    ----------
    df : DataFrame.
        Results of API extraction.
    crs : pyproj.crs.CRS.
       coordinate reference system.
    variable : str, optional.
        Variable of NETCDF.
    delete_orig : bool, optional.
        Set to True to delete original downloaded file (e.g. NetCDF).

    Returns
    -------
    df : DataFrame
        Results with schema for EnerMaps data table

    """
    dicts = []
    for i, row in df.iterrows():
        filename = row["value"]
        if filename.startswith("http"):
            filename = "/vsicurl/" + filename
        if filename[-2:] == "nc":
            src_ds = gdal.Open("NETCDF:{0}:{1}".format(filename, variable))
        else:
            src_ds = gdal.Open(filename)
        source_wkt = src_ds.GetProjectionRef()
        source_crs = CRS.from_wkt(source_wkt)

        dest_wkt = osr.SpatialReference()
        dest_wkt.ImportFromEPSG(crs.to_epsg())
        dest_wkt = dest_wkt.ExportToPrettyWkt()

        ds = gdal.AutoCreateWarpedVRT(src_ds, source_wkt, dest_wkt)
        for b in range(ds.RasterCount):
            my_dict = {}
            b += 1
            dest_filename = Path(filename).stem
            if ds.RasterCount > 1:
                dest_filename += "band" + str(b) + ".tif"
            else:
                dest_filename += ".tif"
            logging.info("Translating band {}".format(b))
            if ds.RasterCount > 1 and crs != source_crs:
                out_ds = gdal.Translate(
                    dest_filename, ds, format="GTiff", bandList=[b], outputSRS=srs
                )
            my_dict["time"] = row["time"] + pd.Timedelta(hours=row["dt"]) * (b - 1)
            my_dict["z"] = row["z"]
            my_dict["dt"] = row["dt"]
            my_dict["unit"] = row["unit"]
            my_dict["variable"] = variable
            logging.info(dest_filename)
            my_dict["FID"] = dest_filename
            my_dict["Raster"] = True
            dicts.append(my_dict)
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
            "unit",
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
    Check whether the dataset exist in any table.
    Parameters
    ----------
    ds_id : int.
    dbURL : str, optional
        The default is "postgresql://test:example@localhost:5433/dataset".
    tables : list of string, optional
        The default is ["datasets", "spatial", "data"].
    Returns
    -------
    bool
    """
    lengths = []
    for table in tables:
        with ps.connect(dbURL) as conn:
            cur = conn.cursor()
            cur.execute(
                sql.SQL("SELECT COUNT(*) FROM {} WHERE ds_id = %(ds_id)s;").format(
                    sql.Identifier(table)
                ),
                {"ds_id": ds_id},
            )
            count = cur.fetchone()[0]
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
        rs = con.execute(
            "DELETE FROM datasets WHERE ds_id = %(ds_id)s;", {"ds_id": ds_id,}
        )


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
    datapackage or None
    """
    engine = sqla.create_engine(dbURL)
    df = pd.read_sql(
        "SELECT * FROM datasets WHERE ds_id = %s", params=(ds_id,), con=engine
    )
    if not df.empty:
        metadata = df.loc[0, "metadata"]
        return metadata.get("datapackage")
    else:
        return None


def download_url(url, save_path, append_path="", chunk_size=128, timeout=10):
    """
    Download file from URL.
    Source: https://stackoverflow.com/a/9419208
    Parameters
    ----------
    url : string
    save_path : string
    append_path: string
        URL complement added after following the url.
        The default is an empty string.
    chunk_size : integer, optional
        The default is 128.
    Returns
    -------
    None.
    """
    r = requests.get(url, allow_redirects=True, stream=True, timeout=timeout)
    if len(append_path) > 0:
        url = r.url + append_path
        r = requests.get(url, stream=True, timeout=timeout)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def get_ld_json(url: str) -> dict:
    """Parse JSON-LD. Source: https://stackoverflow.com/a/59113576."""
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    return json.loads(
        "".join(soup.find("script", {"type": "application/ld+json"}).contents)
    )
