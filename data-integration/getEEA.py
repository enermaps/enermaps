#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 8 11:51:38 2021

@author: giuseppeperonato
"""

import pandas as pd
import utilities
import frictionless
from pandas_datapackage_reader import read_datapackage
import json
import os
import sys
from datetime import datetime
import requests
import zipfile

# In Docker
host = "db"
port = 5432

ds_id = 5

def download_url(url, save_path, append_path="",chunk_size=128, timeout=10):
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
    r = requests.get(url, allow_redirects=True, stream=True,timeout=timeout)
    if len(append_path) > 0:
        url = r.url + append_path
        r = requests.get(url, stream=True, timeout=timeout)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def extractZip(source, target):
    """
    Extract zip.

    Parameters
    ----------
    source : string or path-like object
    target : string

    Returns
    -------
    List of tuples: (extracted file path, date last modified) 

    """
    # Get the file names of extracted files
    zip_ref = zipfile.ZipFile(source, 'r')
    extracted = zip_ref.namelist()
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(target)
    return [(os.path.join(target, x), zip_ref.getinfo(x).date_time)  for x in extracted]

def get(url,path,dp,force=False):
    """
    Retrieves data and check validity/update

    Parameters
    ----------
    url : str
        URL to retrieve the data from.
    path : str
        Target path to save documents.
    dp : frictionless.package
        Datapackage agains which validating the data.
    force : Boolean, optional
        If True, new data will be uploaded even if the same as in the db. The default is False.

    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    frictionless.package
        Pakage descring the data.

    """

    download_url(url[0],"{}.zip".format(path),append_path=url[1])
    filepath, last_modified  = extractZip("{}.zip".format(path),path)[0]

    # Metadata to retrieve from data
    last_modified = datetime(*last_modified).strftime("%Y-%m-%d %H:%M:%S")
    # last_modified = datetime.fromtimestamp(utilities.creation_date(filepath)).strftime('%Y-%m-%d-%H:%M')
    # year = int(filepath.split("/")[-1].split("-")[0])
    
    # Rename the data, so that the path is the same regardless of the version
    os.rename(filepath,os.path.join(path,"data.csv"))
    os.remove("{}.zip".format(path))

    # Inferring and completing metadata
    print("Creating datapackage for input data")
    new_dp = frictionless.describe_package(os.path.join(path,"data.csv"),
                                           stats=True, #Add stats
                                           )
    new_dp.resources[0]["path"] = os.path.join(path,"data.csv")
    # Add date
    new_dp["last_modified"] = last_modified
    # Add groupChar
    new_dp.resources[0].schema.get_field("ValueNumeric").group_char =","
    # new_dp.to_json("{}/datapackage.json".format(path))
    
    # Logic for update
    if dp != None:
        # check stats
        ChangedStats = dp["resources"][0]["stats"] != new_dp["resources"][0]["stats"]
        ChangedDate = dp["last_modified"] != new_dp["last_modified"]

        if ChangedStats or ChangedDate:
            print("Data has changed")
        elif force:
            print("Forced update")
        else:
            print("Data has not changed. Use force update if you want to reupload.")
            return None, None

    dp = new_dp

    val = frictionless.validate(dp)
    if val["valid"]:
        print("Returning valid data")
        data = read_datapackage(dp)
        data.columns = [str(col.strip()) for col in data.columns]
        enermaps_data = pd.DataFrame(columns=["start_at","fields","variable","value","ds_id","fid","dt","z","israster","unit"])
        # Conversion
        enermaps_data["start_at"] = pd.to_datetime(data["Year"],format="%Y")
        enermaps_data["value"] = data.loc[:,data.columns.str.startswith("ValueNumeric")].astype(float)
        enermaps_data["unit"] = data.loc[:,data.columns.str.startswith("Unit")]
        enermaps_data["variable"] = data["Market_Sector"]
        enermaps_data["fid"] = data.loc[:,data.columns.str.startswith("CountryShort")]
        # Constants
        enermaps_data["dt"] = 8760
        enermaps_data["israster"] = False
        # Other fields to json
        other_cols = [x for x in data.columns if x not in ['CountryShort',"ValueNumeric","Unit", "Year"]]
        data["Year"] = data["Year"].astype(int)
        enermaps_data["fields"] = data[other_cols].to_dict(orient="records")
        enermaps_data["fields"] = enermaps_data["fields"].apply(lambda  x: json.dumps(x))
        return enermaps_data, dp
    else:
        print("Data is not valid")
        print(val)
        return None, None


if __name__ == "__main__":
    argv = sys.argv
    if "--force" in argv:
        Force = True
    else:
        Force = True

    if not os.path.exists("data"):
        os.mkdir("data")
    path = os.path.join("data",str(ds_id))
    if not os.path.exists(path):
        os.mkdir(os.path.join(path))
        
    dp = utilities.getDataPackage(ds_id, "postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port))
    
    data, dp = get([
        # "https://www.eea.europa.eu/data-and-maps/data/approximated-estimates-for-the-share-2/eea-2017-res-share-proxies/2016-res_proxies_eea_csv/", #old_data
        "https://www.eea.europa.eu/ds_resolveuid/X8FH9JO6B1", #Permaling to latest version
        "/at_download/file"],
        path=path,
        dp=dp,
        force=Force)
    
    if isinstance(data,pd.DataFrame):
        # Remove existing dataset
        if utilities.datasetExists(ds_id, "postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port)):
            utilities.removeDataset(ds_id, "postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port))
            print("Removed existing dataset")
            
        # Create dataset table
        datasets = pd.read_csv("datasets.csv",engine="python",index_col=[0])
        metadata = datasets.loc[ds_id].fillna("").to_dict()
        metadata["datapackage"] = dp
        metadata = json.dumps(metadata)
        dataset = pd.DataFrame([{"ds_id": ds_id, "metadata":metadata}])
        utilities.toPostgreSQL(dataset,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="datasets")
        
        # Create data table
        data["ds_id"] =  ds_id
        utilities.toPostgreSQL(data,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="data")
    
  
