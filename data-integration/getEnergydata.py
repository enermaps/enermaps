#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom script for retrieving EnergyData records.

@author: giuseppeperonato
"""

import json
import logging
import os
import sys

import pandas as pd
import pandas_datapackage_reader
import requests
import utilities
from bs4 import BeautifulSoup

# Constants
logging.basicConfig(level=logging.INFO)
ID = "5ed45e2a-0291-4338-aeda-46da78470aff"
URL_API = "https://energydata.info/api/3/action/datastore_search?offset={offset}&resource_id={ID}"
URL_METADATA = (
    "https://energydata.info/dataset/world-global-tracking-framework-2017/resource/{ID}"
)

OFFSET = 0  # Start offset from 0 to get the first fields
MAX_REQUESTS = 100  # This seems a limit in the API
DROP_VARS = ["Series Code"]
ID_VARS = ["Series Name", "Country Name", "_id", "Country Code"]
SPATIAL_VARS = ["Country Code"]
ISRASTER = False
DT = 8760
# Country codes that are not recognized as valid ISO3166-1 alpha3 need to be manually converted
EXTRA_COUNTRIES = {
    "ADO": "AD",  # Andorra
    "CHI": "JE",  # Channel Islands
    "ZAR": "CD",  # Congo, Democratic Republic of the
    "IMY": "IM",  # Isle of Man,
    "KSV": "XK",  # Kosovo
    "ANT": "AN",  # Netherlands Antilles
    "ROM": "RO",  # Romania
    "TMP": "TP",  # East Timor
    "WBG": "PS",  # Palestine
}
# In Docker
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


def get(url: str = URL_API, dp: dict = None, force: bool = False):
    """
    Retrieve records from EnergyData API and format them.

    Parameters
    ----------
    url : str, optional
        The default is URL_API.
    dp : dict, optional
        Dictionary containing metadata for update check (not a datapackage). The default is None.
    force : bool, optional
        The default is False.

    Returns
    -------
    enermaps_data : pd.DataFrame
        DF in EnerMaps format.
    new_dp : dict
        Dictionary containing metadata for update check (not a datapackage).

    """
    # First API call to get the nuber of records. The API is limited then to 100 records
    t = requests.get(url.format(offset=OFFSET, ID=ID))
    response = json.loads(t.text)
    total = response["result"]["total"]  # total number of records

    # Loop over batches of 100 records
    records = []
    for i in range(total // MAX_REQUESTS + 1):
        t = requests.get(url.format(offset=i * MAX_REQUESTS, ID=ID))
        response = json.loads(t.text)
        records.append(pd.DataFrame.from_records(response["result"]["records"]))
    records = pd.concat(records, axis=0, ignore_index=True)

    # Convert country code to ISO3166-1 alpha 2
    countries = pandas_datapackage_reader.read_datapackage(
        "https://github.com/datasets/country-codes"
    )
    alpha3_to_2 = dict(
        countries[["ISO3166-1-Alpha-3", "ISO3166-1-Alpha-2"]].to_dict(orient="split")[
            "data"
        ]
    )
    records["Country Code"] = records["Country Code"].replace(alpha3_to_2)
    records["Country Code"] = records["Country Code"].replace(EXTRA_COUNTRIES)

    # Convert to numeric, replacing null values
    records.loc[:, records.columns.str.contains("YR")] = records.loc[
        :, records.columns.str.contains("YR")
    ].replace("..", None)
    records.loc[:, records.columns.str.contains("YR")] = records.loc[
        :, records.columns.str.contains("YR")
    ].apply(lambda x: pd.to_numeric(x), axis=1)

    # Create medatata dict containing the last_updated field
    metadata_table = getMetadata(URL_METADATA)
    last_updated = metadata_table.loc["Last updated"].values[0]
    new_dp = {"last_updated": last_updated}

    if dp is not None:  # Existing dataset
        # check stats
        isChangedDate = dp["last_updated"] != new_dp["last_updated"]
        if isChangedDate:
            logging.info("Data has changed")
            if isValid(records):
                enermaps_data = prepare(records)
        elif isForced:
            logging.info("Forced update")
            if isValid(records):
                enermaps_data = prepare(records)
        else:
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None
    else:  # New dataset
        if isValid(records):
            enermaps_data = prepare(records)

    return enermaps_data, new_dp


def isValid(records: pd.DataFrame) -> bool:
    """Check whether the records are consistent with past scheme. Allow for new year fields to be added."""
    base_fields = ["_id", "Series Name", "Series Code", "Country Name", "Country Code"]
    for field in base_fields:
        assert field in records.columns
    year_fields = [x for x in records.columns if x not in base_fields]
    for field in year_fields:
        assert "[YR" in field
        assert records[field].dtype == "float64"
    return True


def getMetadata(url: str = URL_METADATA) -> pd.DataFrame:
    """Scrape the EnergyData landing page to look for the metadata table."""
    t = requests.get(url.format(ID=ID))
    soup = BeautifulSoup(t.text, "html.parser")

    # get the second table, containing the metadata
    metadata_table = soup.findAll(
        "table", {"class": "table table-striped table-bordered table-condensed"}
    )[-1]
    metadata_table = pd.read_html(str(metadata_table))[0]

    metadata_table = metadata_table.set_index(["Field"])

    # Check for validity
    assert metadata_table.shape == (19, 1)
    assert "Last updated" in metadata_table.index

    return metadata_table


def prepare(data: pd.DataFrame):
    """
    Prepare data in EnerMaps format. Customized for EnergyData.

    Parameters
    ----------
    data : pd.DataFrame
        Data

    Returns
    -------
    DataFrame
        Data in EnerMaps format.

    """
    value_vars = [
        x for x in data.columns if x not in SPATIAL_VARS + ID_VARS + DROP_VARS
    ]

    # Unpivoting
    data = data.melt(id_vars=ID_VARS, value_vars=value_vars)
    # Remove nan
    data = data.dropna()

    # Encoding FID as country code
    data["fid"] = data[SPATIAL_VARS]

    # Conversion
    enermaps_data = pd.DataFrame(
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
    enermaps_data["fid"] = data["fid"]
    enermaps_data["value"] = data["value"]
    enermaps_data["variable"] = data["Series Name"].str.split("(", expand=True)[0]
    enermaps_data["start_at"] = pd.to_datetime(
        data.variable.str.split(" ", expand=True)[0]
    )
    enermaps_data["unit"] = data["Series Name"].str.split("(", expand=True)[1].str[:-1]
    enermaps_data["dt"] = DT
    enermaps_data["israster"] = ISRASTER

    return enermaps_data


if __name__ == "__main__":
    argv = sys.argv
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_id = int(
        datasets[datasets["di_script"] == os.path.basename(argv[0])].index.values[0]
    )
    url = datasets.loc[
        datasets["di_script"] == os.path.basename(argv[0]), "di_URL"
    ].values[0]

    if "--force" in argv:
        isForced = True
    else:
        isForced = True
    dp = utilities.getDataPackage(ds_id, DB_URL)

    data, dp = get(url=url, dp=dp, force=isForced)

    if isinstance(data, pd.DataFrame):
        # Remove existing dataset
        if utilities.datasetExists(ds_id, DB_URL):
            utilities.removeDataset(ds_id, DB_URL)
            logging.info("Removed existing dataset")

        # Create dataset table
        metadata = datasets.loc[ds_id].fillna("").to_dict()
        metadata["datapackage"] = dp
        metadata = json.dumps(metadata)
        dataset = pd.DataFrame([{"ds_id": ds_id, "metadata": metadata}])
        utilities.toPostgreSQL(
            dataset, DB_URL, schema="datasets",
        )

        # Create data table
        data["ds_id"] = ds_id
        utilities.toPostgreSQL(
            data, DB_URL, schema="data",
        )
