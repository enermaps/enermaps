#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:18:50 2021

@author: giuseppeperonato
"""

import pandas as pd
import requests
import subprocess
import os
import utilities
import logging

# Constants
DS_ID = 25
Force = False #Force update
logging.basicConfig(level=logging.INFO)
# In Docker
host = "enermaps_db_1"
port = 5432
# Local
# host = "localhost"
# port = 5433


def get(timeseries: pd.core.indexes.datetimes.DatetimeIndex=pd.date_range("2009-12-30",periods=1),
        timestep: float=0.5, heights: list=[100], variable: str="PD", Run: bool=False):
    """
    API for the New European Wind Atlas
    https://map.neweuropeanwindatlas.eu

    Parameters
    ----------
    timeseries : Pandas date_range, optional
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
    logging.basicConfig(level=logging.INFO)
    HEIGHT_LEVELS = [50, 75, 100, 150, 200, 250, 500]
    
    dicts = []
    for time in timeseries:
        year = time.year
        month = time.month
        day = time.day
        ts = int(timestep * 2)
        if ts > 47:
            ts = 47
        if ts < 1:
            ts = 0.5
        for height in heights:
            h = HEIGHT_LEVELS.index(height)
            URL = "http://opendap.neweuropeanwindatlas.eu:80/opendap/newa/NEWA_MESOSCALE_ATLAS/"
            URL += "{year}/NEWA-{year}-{month}-{day}.nc.nc?PD[0:{ts}:47][{h}:1:{h}][0:1:1381][0:1:1597]".format(
                year=year, month=month, day=day, ts=ts, h=h
            )
            filename = "NEWA-{year}-{month}-{day}_{height}m_{ts}min.nc".format(
                year=year, month=month, day=day, height=height, ts=int(timestep * 60)
            )
            if Run:
                logging.info("Requesting: {}".format(URL))
                h = requests.head(URL)
                if h.status_code == 200:
                    # Issue about the server pretending to send gzip, patched as here:
                    # https://github.com/psf/requests/issues/3849#issuecomment-277196788
                    r = requests.get(URL, allow_redirects=True, headers={'Accept-Encoding': 'identity'})
                    with open(filename, "wb") as f:
                        f.write(r.content)
                    dicts.append({"time": time, "dt": timestep, "z": height, "value": filename})
                else:
                    dicts.append({"value": None})
            else:
                logging.info("URL to be requested: {}".format(URL))

    df = pd.DataFrame(dicts)
    return df

if __name__ == "__main__":
    argv = sys.argv
    if "--force" in argv:
        Force = True

    period = pd.date_range("2018-12-30",periods=1)
    rasters = get(period,Run=True)
    data = utilities.prepareRaster(rasters, variable = "PD", delete_orig=True)
    
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists(os.path.join("data",str(DS_ID))):
        os.mkdir(os.path.join("data",str(DS_ID)))
    for i, row in data.iterrows():
        os.rename(row.FID, os.path.join("data", str(DS_ID), row.FID))
    
    if utilities.datasetExists(DS_ID) and Force==False:
        logging.warning("Dataset already exists. Use force update to replace.")
    else:
        if utilities.datasetExists(DS_ID):
            utilities.removeDataset(DS_ID)
            logging.info("Removed existing dataset")
        # Create dataset table
        datasets = pd.read_csv("datasets.csv",engine="python",index_col=[0])
        dataset = pd.DataFrame([{"ds_id": DS_ID, "metadata":datasets.loc[DS_ID].to_json()}])
        utilities.toPostgreSQL(dataset,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="datasets")
        
        # Create data table
        data["ds_id"] =  DS_ID
        utilities.toPostgreSQL(data,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="data")
        
        #Create empty spatial table
        spatial = pd.DataFrame()
        spatial[["FID","ds_id"]] = data[["FID","ds_id"]]
        utilities.toPostgreSQL(spatial,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="spatial")


