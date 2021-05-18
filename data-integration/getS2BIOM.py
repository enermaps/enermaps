#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom script for S2DBIOM dataset.

Created on Tue May 18 10:26:46 2021

@author: giuseppeperonato
"""

import json
import logging
import os
import sys

import pandas as pd
import utilities

# Constants
logging.basicConfig(level=logging.INFO)
ISRASTER = False

COUNTRIES = [
    "AT",
    "BE",
    "BG",
    "HR",
    "CY",
    "CZ",
    "DK",
    "EE",
    "FI",
    "FR",
    "DE",
    "EL",
    "HU",
    "IE",
    "IT",
    "LV",
    "LT",
    "LU",
    "LV",
    "LT",
    "LU",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SK",
    "SI",
    "ES",
    "SE",
    "UK",
    "AL",
    "BA",
    "KS",
    "MK",
    "MD",
    "ME",
    "RS",
    "TR",
    "UA",
]
ABBREVIATIONS = {
    "dm": "Dry Mass",
    "rs": "Road Side Cost",
    "euro": "Euro/ton dry mass",
    "kton": "kton dry mass",
    "BASE": "Base potential",
    "TECH": "Technical potential",
    "UD1": "User-defined potential 1",
    "UD2": "User-defined potential 2",
    "UD3": "User-defined potential 3",
    "UD4": "User-defined potential 4",
    "UD5": "User-defined potential 5",
    "UD6": "User-defined potential 6",
    "UD7": "User-defined potential 7",
    "UD8": "User-defined potential 8",
    "HIGH": "High potential",
}

COUNTRIES_TO_ISO = {"KS": "XK", "EL": "GR", "UK": "GB"}

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


def get(url: str) -> pd.DataFrame:
    """
    Parse original Excel file and returns df in EnerMaps schema.

    Parameters
    ----------
    url : str
        Download url with {} for country code.

    Returns
    -------
    enermaps_data : pd.DataFrame
        Data in EnerMaps schema.

    """
    dfs = []
    for country_code in COUNTRIES:
        url = url.format(country_code)
        logging.info("Downloading {}".format(country_code))
        try:
            sheets = pd.read_excel(url, sheet_name=None)
            for sheet_name in list(sheets.keys())[2:]:
                sheet = sheets[sheet_name]
                if sheet.shape[0] > 0:
                    columns = list(sheet.columns)
                    columns[0] = "nuts"
                    sheet.columns = columns
                    parameter, potential, year, unit = sheet_name.split("_")
                    sheet["parameter"] = parameter
                    sheet["potential"] = potential
                    sheet["start_at"] = pd.to_datetime(year)
                    sheet["unit"] = unit
                    id_vars = [x for x in sheet.columns if x not in columns[1:]]
                    data = sheet.melt(id_vars=id_vars, value_vars=columns[1:])
                    data["variable"] = data["variable"].astype(int)
                    dfs.append(data)
        except IOError:
            logging.error("File not found")
    data = pd.concat(dfs, ignore_index=True)

    # Get the keys of the variable encoding
    keys = sheets["readme"].iloc[26:76, :7]
    keys.columns = keys.iloc[0, :]
    keys = keys.set_index("type_id")
    keys = keys.iloc[1:, :]

    data = data.replace(ABBREVIATIONS)
    data["nuts"] = data["nuts"].replace(COUNTRIES_TO_ISO)
    data["variable"] = data["variable"].replace(keys.to_dict()["type_name"])
    data["variable"] = (
        data["potential"].astype(str) + " : " + data["variable"].astype(str)
    )
    data["fields"] = data[["parameter", "potential"]].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x))

    # Remove nan
    data = data.dropna()

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
    enermaps_data["fid"] = data["nuts"]
    enermaps_data["value"] = data["value"]
    enermaps_data["variable"] = data["variable"]
    enermaps_data["fields"] = data["fields"]
    enermaps_data["unit"] = data["unit"]
    enermaps_data["start_at"] = data["start_at"]
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
        isForced = False

    data = get(url=url)

    # Remove existing dataset
    if utilities.datasetExists(ds_id, DB_URL) and not isForced:
        raise FileExistsError("Use --force to replace the existing dataset.")
    elif utilities.datasetExists(ds_id, DB_URL) and isForced:
        utilities.removeDataset(ds_id, DB_URL)
        logging.info("Removed existing dataset")
    else:
        pass

    # Create dataset table
    metadata = datasets.loc[ds_id].fillna("").to_dict()
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
