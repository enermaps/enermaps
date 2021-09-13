#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:18:50 2021

@author: giuseppeperonato
"""
import argparse
import json
import logging
import os
import sys
import zipfile
from pathlib import Path

import frictionless
import geopandas as gpd
import pandas as pd
import psycopg2 as ps
import requests
import sqlalchemy as sqla
import validators
from bs4 import BeautifulSoup
from osgeo import gdal, osr
from psycopg2 import sql
from pyproj import CRS

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")

DB_URL = "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
    DB_HOST=DB_HOST,
    DB_PORT=DB_PORT,
    DB_USER=DB_USER,
    DB_PASSWORD=DB_PASSWORD,
    DB_DB=DB_DB,
)

ENERMAPS_DF = pd.DataFrame(
    columns=[
        "start_at",
        "fields",
        "variable",
        "value",
        "ds_id",
        "fid",
        "dt",
        "z",
        "israster",
        "unit",
    ]
)

DT_FORMAT = "%Y-%m-%d %H:%M"


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
    isNC = False
    for i, row in df.iterrows():
        filename_orig = row["value"]
        if filename_orig.startswith("http"):
            filename = "/vsicurl/" + filename_orig
        if filename_orig[-2:] == "nc":
            isNC = True
            filename = "NETCDF:{0}:{1}".format(filename_orig, variable)
        else:
            filename = filename_orig
        # Override function parameter
        if "variable" in row.index:
            variable = row["variable"]

        src_ds = gdal.Open(filename)

        # Override function parameter
        if "variable" in row.index:
            variable = row["variable"]

        if "crs" in df.columns:
            source_wkt = osr.SpatialReference()
            source_wkt.ImportFromEPSG(row.crs.to_epsg())
            source_wkt = source_wkt.ExportToPrettyWkt()
            source_crs = CRS.from_wkt(source_wkt)
        else:
            prj = src_ds.GetProjection()
            srs = osr.SpatialReference(wkt=prj)
            source_crs = CRS.from_epsg(srs.GetAttrValue("authority", 1))

        dest_wkt = osr.SpatialReference()
        dest_wkt.ImportFromEPSG(crs.to_epsg())
        dest_wkt = dest_wkt.ExportToPrettyWkt()
        if src_ds is not None:
            for b in range(src_ds.RasterCount):
                my_dict = {}
                b += 1
                dest_filename = Path(filename).stem
                dest_filename += "_band" + str(b)

                # Translating to make sure that the raster settings are consistent for each band
                logging.info("Translating band {}".format(b))
                os.system(  # nosec
                    "gdal_translate {filename} {dest_filename}.tif -b {b} -of GTIFF --config GDAL_PAM_ENABLED NO -co COMPRESS=DEFLATE -co BIGTIFF=YES".format(
                        filename=filename, dest_filename=dest_filename, b=b
                    )
                )

                # Reprojecting if needed
                if source_crs.to_epsg() != crs.to_epsg():
                    logging.info(
                        "Warping from {} to {}".format(
                            source_crs.to_epsg(), crs.to_epsg()
                        )
                    )
                    translated = dest_filename + ".tif"  # from previous step
                    warped = dest_filename + "_warped.tif"
                    dest_filename += "_{}".format(crs.to_epsg())
                    os.system(  # nosec
                        "gdalwarp {source} {dest} -of GTIFF -s_srs {sourceSRS} -t_srs {outputSRS} --config GDAL_PAM_ENABLED NO -co COMPRESS=DEFLATE -co BIGTIFF=YES".format(
                            source=translated,
                            dest=warped,
                            outputSRS=crs.to_string(),
                            sourceSRS=source_crs.to_string(),
                        )
                    )
                    # Get metadata for checking offset and scale parameters
                    metadata = json.loads(
                        os.popen("gdalinfo {} -json".format(filename)).read()  # nosec
                    )
                    metadata = metadata["bands"][b - 1]
                    if all(k in metadata for k in ("offset", "scale")):
                        # Offset and scale are not handled by gdalwarp https://gis.stackexchange.com/a/229954
                        offset, scale = metadata["offset"], metadata["scale"]
                        os.system(  # nosec
                            "{python_dir}/gdal_calc.py -A {source} --outfile={dest}.tif --type='Float32' --calc=\"A*{scale}+{offset}\"".format(
                                python_dir=os.path.dirname(sys.executable),
                                source=warped,
                                dest=dest_filename,
                                offset=offset,
                                scale=scale,
                            )
                        )
                        os.remove(translated)
                        os.remove(warped)
                    else:
                        os.rename(warped, dest_filename + ".tif")

                dest_filename += ".tif"
                logging.info(dest_filename)
                if row["dt"] == 720 and row["start_at"] is not None:  # month case
                    month_count = b - 1  # starting at 0
                    month_number = month_count % 12 + 1  # 1-12
                    year = row["start_at"].year + month_count // 12
                    date = pd.to_datetime("{}-{}".format(year, month_number))
                    if month_number == 12:
                        month_number = 0
                        year += 1
                    date_future = pd.to_datetime("{}-{}".format(year, month_number + 1))
                    my_dict["dt"] = (date_future - date).total_seconds() / 3600
                    my_dict["start_at"] = date
                else:
                    my_dict["start_at"] = row["start_at"] + pd.Timedelta(
                        hours=row["dt"]
                    ) * (b - 1)
                    my_dict["dt"] = row["dt"]
                my_dict["z"] = row["z"]
                my_dict["unit"] = row["unit"]
                my_dict["variable"] = variable
                my_dict["fid"] = dest_filename
                my_dict["israster"] = True
                if isNC:
                    my_dict["fields"] = json.dumps(nc_metadata(filename_orig, variable))
                dicts.append(my_dict)
        else:
            logging.error("Cannot open file.")
        if delete_orig:
            os.remove(filename_orig)
    data = pd.DataFrame(
        dicts,
        columns=[
            "start_at",
            "fields",
            "variable",
            "value",
            "ds_id",
            "fid",
            "dt",
            "z",
            "unit",
            "israster",
        ],
    )
    return data


def toPostgreSQL(
    df: pd.DataFrame,
    dbURL: str = "postgresql://postgres:postgres@localhost:5432/dataset",
    schema: str = "data",
    chunksize: int = 10000,
):
    """Load non-spatial data to pgsql."""
    db_engine = sqla.create_engine(dbURL)
    logging.info("Loading to PostgreSQL...")
    df.to_sql(schema, db_engine, if_exists="append", index=False, chunksize=chunksize)
    logging.info("Done.")


def toPostGIS(
    gdf: gpd.GeoDataFrame,
    dbURL: str = "postgresql://postgres:postgres@localhost:5432/dataset",
    schema: str = "spatial",
):
    """Load spatial data to pgsql."""
    db_engine = sqla.create_engine(dbURL)
    logging.info("Loading to PostGIS...")
    gdf.to_postgis(schema, db_engine, if_exists="append", index=False)
    logging.info("Done.")


def datasetExists(
    ds_id, dbURL=DB_URL, tables=["datasets", "spatial", "data"],
):
    """
    Check whether the dataset exist in any table.

    Parameters
    ----------
    ds_id : int.
    dbURL : str, optional
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


def removeDataset(ds_id, dbURL=DB_URL):
    """
    Delete the dataset.

    Parameters
    ----------
    ds_id : int.
    dbURL : str, optional

    Returns
    -------
    None
    """
    engine = sqla.create_engine(dbURL)
    with engine.connect() as con:
        con.execute(
            "DELETE FROM datasets WHERE ds_id = %(ds_id)s;", {"ds_id": ds_id},
        )


def getDataPackage(ds_id, dbURL=DB_URL):
    """
    Retrieve the datapackage.

    Parameters
    ----------
    ds_id : int.
    dbURL : str, optional

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


def download_url(url, save_path, chunk_size=128, timeout=10):
    """
    Download file from URL. Source: https://stackoverflow.com/a/9419208.

    Parameters
    ----------
    url : string
    save_path : string
    chunk_size : integer, optional
        The default is 128.

    Returns
    -------
    None.
    """
    if validators.url(url):
        r = requests.get(url, allow_redirects=True, stream=True, timeout=timeout)
        if r.status_code == 200:
            with open(save_path, "wb") as fd:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
        else:
            logging.error("Error retrieving the URL")
    else:
        logging.error("URL not valid")


def get_ld_json(url: str) -> dict:
    """Parse JSON-LD. Source: https://stackoverflow.com/a/59113576."""
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    return json.loads(
        "".join(soup.find("script", {"type": "application/ld+json"}).contents)
    )


def getGitHub(user: str, repo: str, request="content", path="", branch="master"):
    """
    Obtain metadata from GitHub.

    Parameters
    ----------
    user : str
    repo : str
    request : str, optional
        Choose from "content", "date", "version". Default is "content".
    path : str, optional
        Default is "".
    branch : str, optional
        Default is "master".

    Returns
    -------
    str
    """
    raw_content = "https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}".format(
        user=user, repo=repo, branch=branch, path=path
    )
    api = "https://api.github.com/repos/{user}/{repo}/commits?sha=master&path={path}".format(
        user=user, repo=repo, path=path
    )
    commits = requests.get(api).json()
    if request == "content":
        return raw_content
    if request == "date":
        return commits[0]["commit"]["author"]["date"]
    if request == "version":
        return commits[0]["sha"]


def extractZip(source, target):
    """
    Extract zip.

    Parameters
    ----------
    source : string or path-like object
    target : string

    Returns
    -------
    List of strings: extracted file path

    """
    # Get the file names of extracted files
    zip_ref = zipfile.ZipFile(source, "r")
    extracted = zip_ref.namelist()
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(target)
    return [os.path.join(target, x) for x in extracted]


def full_country_to_code(
    countries: pd.Series,
    dbURL: str = "postgresql://test:example@localhost:5433/dataset",
):
    """
    Convert full Country names to ISO 3166-1 alpha2 codes.

    Parameters
    ----------
    countries : pd.Series
        Full contry names.
    dbURL : str, optional
        The default is "postgresql://test:example@localhost:5433/dataset".

    Returns
    -------
    pd.Series
        ISO 3166-1 alpha2 codes.

    """
    db_engine = sqla.create_engine(dbURL)
    try:
        table = pd.read_csv("country_codes.csv", index_col=0)
    except FileNotFoundError:
        table = pd.read_sql(
            "SELECT * from public.spatial WHERE levl_code = 'country'", db_engine
        )
        table = table[["name_engl", "cntr_code"]]
        table.to_csv("country_codes.csv")
    transl = table.set_index("name_engl").T.to_dict(orient="records")[0]
    return countries.replace(transl)


def nc_metadata(file: str, variable: str) -> dict:
    """
    Extract NetCDF metadata using gdalinfo
    """
    gdalinfo = os.popen("gdalinfo NETCDF:{}:{}".format(file, variable)).read()  # nosec
    nc_metadata = [
        x.split("#")[1].split("=") for x in gdalinfo.split("\n") if "NC_GLOBAL" in x
    ]
    var_metadata = [
        x.split("#")[1].split("=")
        for x in gdalinfo.split("\n")
        if x.startswith("  {}".format(variable))
    ]
    dict_metadata = dict()
    all_metadata = nc_metadata + var_metadata
    for x in all_metadata:
        dict_metadata[x[0]] = x[1]
    return dict_metadata


def isDPvalid(dp: frictionless.package.Package, new_dp: frictionless.package.Package):
    """
    Check whether the new DataPackage is valid and make sure the schema has not changed.
    Parameters
    ----------
    dp : frictionless.package.Package
        Original datapackage
    new_dp : frictionless.package.Package
        Datapackage describing the new loaded data
    Returns
    -------
    Boolean
    """
    val = frictionless.validate(new_dp)
    if (
        val["valid"]
        and dp["resources"][0]["schema"] == new_dp["resources"][0]["schema"]
    ):
        logging.info("Returning valid and schema-compliant data")
        return True
    else:
        logging.error("Data is not valid or the schema has changed")
        print(val)
        return False


def parser(script_name: str, datasets=pd.DataFrame):
    """Parse arguments used in data-integration pipelines."""
    ds_ids = datasets[datasets["di_script"] == script_name].index
    isForced = False  # initialize
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Import dataset")
        parser.add_argument("--force", action="store_const", const=True, default=False)
        parser.add_argument(
            "--select_ds_ids", action="extend", nargs="+", type=int, default=[]
        )
        args = parser.parse_args()
        isForced = args.force
        if len(args.select_ds_ids) > 0:
            ds_ids = args.select_ds_ids
    return ds_ids, isForced


def get_query_metadata(
    data: pd.DataFrame, selected_fields: list = [], custom_parameters={}
):
    """
    Prepare metadata needed for construct a db query.
    The metadata contain possible parameter values and the default values.

    Parameters
    ----------
    data : pd.DataFrame
        Data using the EnerMaps schema.
    selected_fields : list, optional.
        The keys in the "fields" column that are actually used in the query.
    custom_fields : dict, optional.
        Additional custom parameters.
    Returns
    -------
    parameters : dict
        Possible parameter values to be used in the query.
    default_parameters : dict
        Default parameter values to be used in the query.
    """
    logging.info("Creating query metadata")

    # Set parameter values (unique values)
    parameters = custom_parameters
    data.loc[data["fields"].isnull(), "fields"] = "{}"
    fields = data["fields"].apply(lambda x: json.loads(x))
    fields_df = pd.json_normalize(fields)
    # Restrict parameters to only some fields
    if selected_fields:
        fields_df = fields_df[selected_fields]
    parameters["fields"] = {
        column: fields_df[column].unique().tolist() for column in fields_df.columns
    }
    parameters["variables"] = list(data["variable"].unique())
    parameters["start_at"] = data["start_at"].max().strftime(DT_FORMAT)
    parameters["end_at"] = data["start_at"].min().strftime(DT_FORMAT)
    # Add custom time periods
    if parameters.get("temporal_granularity") == "custom":
        parameters["time_periods"] = list(
            pd.Series(data["start_at"].unique()).dt.strftime(DT_FORMAT)
        )

    # Set default parameters (corresponding to the first record)
    default_parameters = {}
    default_fields = json.loads(data["fields"].iloc[0])
    if selected_fields:
        default_parameters["fields"] = {
            key: default_fields[key] for key in selected_fields
        }
    else:
        default_parameters["fields"] = default_fields
    default_parameters["start_at"] = data["start_at"].iloc[0].strftime(DT_FORMAT)
    default_parameters["variables"] = data["variable"].iloc[0]

    return parameters, default_parameters
