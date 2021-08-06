#!/usr/bin/env python3
"""
Get fresh water use from the European energy sector from Zenodo,
without checking for updates (ended project).

@author: giuseppeperonato
"""
import json
import logging
import os
import sys

import pandas as pd
import requests
import utilities

# Constants
logging.basicConfig(level=logging.INFO)
ISRASTER = False

DB_URL = utilities.DB_URL


def get(url: str) -> pd.DataFrame:
    """
    Parse original Excel file and returns df in EnerMaps schema.

    Parameters
    ----------
    url : str
        Zenodo API url.

    Returns
    -------
    enermaps_data : pd.DataFrame
        Data in EnerMaps schema.

    """
    r = requests.get(url)
    if r.ok:
        metadata = r.json()
        file = metadata["files"][-1]["links"]["self"]

        dfs = []

        sheets = pd.read_excel(file, sheet_name=None, index_col=0)
        for sheetname in list(sheets.keys())[1:]:  # skip summary first sheet
            sheet = sheets[sheetname]
            start_consumption = list(sheet.columns).index("Water consumption") + 1
            start_withdrawal = list(sheet.columns).index("Water withdrawal") + 1

            nuts = sheet.iloc[:, 0]

            consumption = sheet.iloc[:, start_consumption : start_consumption + 9]
            consumption.columns = [
                "Unit",
                2015,
                2020,
                2025,
                2030,
                2035,
                2040,
                2045,
                2050,
            ]
            consumption["nuts"] = nuts
            withdrawal = sheet.iloc[:, start_withdrawal : start_withdrawal + 9]
            withdrawal.columns = [
                "Unit",
                2015,
                2020,
                2025,
                2030,
                2035,
                2040,
                2045,
                2050,
            ]
            withdrawal["nuts"] = nuts

            consumption = consumption.melt(id_vars=["Unit", "nuts"], var_name="Date")
            consumption["Variable"] = sheetname + " - Water consumption"
            consumption["Date"] = pd.to_datetime(consumption["Date"], format="%Y")
            withdrawal = withdrawal.melt(id_vars=["Unit", "nuts"], var_name="Date")
            withdrawal["Date"] = pd.to_datetime(withdrawal["Date"], format="%Y")
            withdrawal["Variable"] = sheetname + " - Water withdrawal"
            dfs.append(consumption)
            dfs.append(withdrawal)

        data = pd.concat(dfs, ignore_index=True)
        # Remove nan
        data = data.dropna()

        # Conversion
        enermaps_data = utilities.ENERMAPS_DF
        enermaps_data["fid"] = data["nuts"]
        enermaps_data["value"] = data["value"]
        enermaps_data["variable"] = data["Variable"]
        enermaps_data["unit"] = data["Unit"]
        enermaps_data["start_at"] = data["Date"]
        enermaps_data["israster"] = ISRASTER

        return enermaps_data


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)
    url = datasets.loc[
        datasets["di_script"] == os.path.basename(sys.argv[0]), "di_URL"
    ].values[0]

    for ds_id in ds_ids:

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
