#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom script to recover results from ENER/C2/2014-641 project.

Only WP3 results are integrated (scenarios up to 2020 and 2030).
The files must be manually downloaded  to be integrated

Created on Tue Jun  1 13:47:49 2021

@author: giuseppeperonato
"""

import json
import logging
import os
import sys
from typing import Tuple

import pandas as pd
import utilities

# Constants
logging.basicConfig(level=logging.INFO)
N_FILES = 14
SPATIAL = ["CO_ID"]
TIME = ["Year"]
TRANSL = {"EL": "GR", "UK": "GB"}
UNIT = "TWh"
ISRASTER = False
DT = 8760
FIELDS = ["Scenario", "Sector", "Sub-sector", "Energy Carrier", "Energy type"]

VARIABLES = {
    "MappingHC Total": "Total Heating and Cooling",
    "H: Heating": "Heating",
    "C: Cooling": "Cooling",
    "Space heating total": "Space heating",
    "Water heating total": "Water heating",
    "Process heating total": "Process heating",
    "Process cooling total": "Process cooling",
    "Space cooling total": "Space cooling",
}

FILES = {
    "WP3_DataAnnex_FinalEnergy_ForPublication_201607.xlsx": "Final Energy",
    "WP3_DataAnnex_PrimaryEnergy_ForPublication_201607.xlsx": "Primary Energy",
    "WP3_DataAnnex_UsefulEnergy_ForPublication_201607.xlsx": "Useful Energy",
}

DB_URL = utilities.DB_URL


def get(directory: str) -> Tuple[pd.DataFrame, dict]:
    """
    Parse original Excel file and returns df in EnerMaps schema.

    Parameters
    ----------
    directory : str
        Path where the Excel files are stored

    Returns
    -------
    enermaps_data : pd.DataFrame
        Data in EnerMaps schema.

    parameters : dict
        Unique parameters to be queried in the "fields".

    """
    data = []
    for file in FILES.keys():
        path = os.path.join(directory, file)
        for sheet in range(2, 6):
            sheet = pd.read_excel(path, sheet_name=sheet)
            sheet = sheet.iloc[1:, :-7]
            sheet["Energy type"] = FILES[file]
            data.append(sheet)

    data = pd.concat(data, ignore_index=True)
    data[SPATIAL] = data[SPATIAL].replace(TRANSL)
    data = data.melt(id_vars=FIELDS + SPATIAL + TIME, value_vars=VARIABLES.keys())

    data["variable"] = data["variable"].replace(VARIABLES)
    data["variable"] = data["Energy type"] + " | " + data["variable"]

    # Remove nan
    data = data.loc[~data["value"].isnull(), :]
    data = data.where(data.notnull(), None)

    # Retrieve parameters from unique fields
    parameters = data[FIELDS].apply(lambda x: list(pd.unique(x)), axis=0).to_dict()

    # Make extra fields in JSON
    data["fields"] = data[FIELDS].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x))

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
    enermaps_data["fid"] = data[SPATIAL].iloc[:, 0]
    enermaps_data["value"] = data["value"]
    enermaps_data["fields"] = data["fields"]
    enermaps_data["variable"] = data["variable"]
    enermaps_data["unit"] = UNIT
    enermaps_data["start_at"] = pd.to_datetime(data["Year"], format="%Y")
    enermaps_data["israster"] = ISRASTER
    enermaps_data["dt"] = DT

    return enermaps_data, parameters


if __name__ == "__main__":
    argv = sys.argv
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_id = int(
        datasets[datasets["di_script"] == os.path.basename(argv[0])].index.values[0]
    )

    if "--force" in argv:
        isForced = True
    else:
        isForced = False

    files_dir = os.path.join("data", str(ds_id))
    if os.path.exists(files_dir) and len(os.listdir(files_dir)) == N_FILES:

        data, parameters = get(files_dir)

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
        # Add parameters as metadata
        metadata["parameters"] = parameters
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
