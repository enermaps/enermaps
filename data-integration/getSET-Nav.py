#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jhj.

Created on Mon May 31 18:04:18 2021

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
VARIABLE = ["Parameter"]
FIELDS = [
    "Scenario",
    "Sector",
    "Perspective",
    "Supertype",
    "Type",
    "Technology",
    "Specification",
    "Fuel",
]


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


def get(directory: str) -> pd.DataFrame:
    """
    Parse original Excel file and returns df in EnerMaps schema.

    Parameters
    ----------
    directory : str
        Path where the Excel files are stores

    Returns
    -------
    enermaps_data : pd.DataFrame
        Data in EnerMaps schema.

    """
    energy = pd.read_excel(
        os.path.join(directory, "1557750718403-Invert_EE-lab_energy_demand_v1.0.xlsm"),
        skiprows=5,
        header=0,
    )
    costs = pd.read_excel(
        os.path.join(directory, "1557750689653-Invert_EE-lab_costs_v1.0.xlsm"),
        skiprows=5,
        header=0,
    )

    data = pd.concat([energy, costs], ignore_index=True)
    data = data.iloc[:, :-3]

    # Remove nan
    data = data.loc[~data["Value"].isnull(), :]
    data = data.where(data.notnull(), None)

    # Make extra fields in JSON
    data["fields"] = data[FIELDS].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x))

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
    enermaps_data["fid"] = data["Country"]
    enermaps_data["value"] = data["Value"]
    enermaps_data["fields"] = data["fields"]
    enermaps_data["variable"] = data[VARIABLE].astype(str).agg(" | ".join, axis=1)
    enermaps_data["unit"] = data["Unit"]
    enermaps_data["start_at"] = pd.to_datetime(data["Year"], format="%Y")
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

    files_dir = os.path.join("data", str(ds_id))
    if os.path.exists(files_dir) and len(os.listdir(files_dir)) == 2:

        data = get(files_dir)

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
    else:
        logging.error("You must manually download the source files.")
