#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:18:50 2021

@author: giuseppeperonato
"""


import pandas as pd
import requests
import subprocess
from osgeo import gdal, osr
import os
import utilities

def get(time="2009-12-30", timestep=0.5, heights=[100], variable="PD", Run=False):
    """
    API for the New European Wind Atlas
    https://map.neweuropeanwindatlas.eu

    Parameters
    ----------
    time : list of years, or datetime, optional
        DESCRIPTION. The default is "2009-12-30".
    variable : string, optional
        DESCRIPTION. The default is "PD".
    timestep : float or int, optional
        DESCRIPTION. The default is 0.5.
    heights : list of ints, optional
        DESCRIPTION. The default is [100].
    Run : boolean, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    df : DataFrame
        Results

    """
    # files = []
    timeseries = []
    dicts = []
    if isinstance(time, list):
        for year in time:
            timeseries.extend(
                pd.date_range(
                    "01.01.{}".format(year), end="31.12.{}".format(year), freq="D"
                ).to_list()
            )
    else:
        timeseries = [time]

    for time in timeseries:
        time = pd.to_datetime(time)
        year = time.year
        month = time.month
        day = time.day
        height_levels = [50, 75, 100, 150, 200, 250, 500]
        ts = int(timestep * 2)
        if ts > 47:
            ts = 47
        if ts < 1:
            ts = 0.5
        for height in heights:
            h = height_levels.index(height)
            URL = "http://opendap.neweuropeanwindatlas.eu:80/opendap/newa/NEWA_MESOSCALE_ATLAS/"
            URL += "{year}/NEWA-{year}-{month}-{day}.nc.nc?PD[0:{ts}:47][{h}:1:{h}][0:1:1381][0:1:1597]".format(
                year=year, month=month, day=day, ts=ts, h=h
            )
            filename = "NEWA-{year}-{month}-{day}_{height}m_{ts}min.nc".format(
                year=year, month=month, day=day, height=height, ts=int(timestep * 60)
            )
            # files.append(filename)
            if Run:
                print("Requesting", URL)
                # Issue about the server pretending to send gzip, patched as here:
                # https://github.com/psf/requests/issues/3849#issuecomment-277196788
                r = requests.get(URL, allow_redirects=True, headers={'Accept-Encoding': 'identity'})
                open(filename, "wb").write(r.content)
            else:
                print("URL to be requested:", URL)

            dicts.append({"time": time, "dt": timestep, "z": height, "value": filename})
    df = pd.DataFrame(dicts)
    return df

if __name__ == "__main__":
    ds_id = 25
    host = "enermaps_db_1"
    port = 5432
    rasters = get(Run=True)
    data = utilities.prepareRaster(rasters, variable = "PD", delete_orig=True)
    if not os.path.exists("data"):
        os.mkdir(data)
    if not os.path.exists(os.path.join("data",str(ds_id))):
        os.mkdir(os.path.join("data",str(ds_id)))
    for i, row in data.iterrows():
        os.rename(row.FID, os.path.join("data", str(ds_id), row.FID))
        
    datasets = pd.read_csv("datasets.csv",engine="python",index_col=[0])
    dataset = pd.DataFrame([{"ds_id": ds_id, "metadata":datasets.loc[ds_id].to_json()}])
    utilities.toPostgreSQL(dataset,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="datasets")
    
    data["ds_id"] =  ds_id
    utilities.toPostgreSQL(data,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="data")

