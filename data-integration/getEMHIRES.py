#!/usr/bin/env python3
"""
Get EMIHIRES dataset from Zenodo.
Do not check for updates (ended project).

@author: giuseppeperonato
"""
import json
import logging
import os
import shutil
import sys

import pandas as pd
import requests
import utilities

# Constants
logging.basicConfig(level=logging.INFO)
ISRASTER = False
START_DATE = "1986-01-01"

DATASETS = {
    17: {
        "file": "EMHIRESPV_NUTS2_level.zip",
        "variable": "PV power capacity factor",
        "unit": "[-]",
        "time_variable": "time_step",
    },
    16: {
        "file": "EMHIRES_WIND_NUTS2_June2019.zip",
        "variable": "Wind power capacity factor",
        "unit": "[-]",
        "time_variable": "Time step",
    },
}

QUERY_FIELDS = {
    17: None,
    16: None,
}

QUERY_PARAMETERS = {
    17: {"temporal_granularity": "hour", "is_tiled": False, "is_raster": False},
    16: {"temporal_granularity": "hour", "is_tiled": False, "is_raster": False},
}

DB_URL = utilities.DB_URL


def get(url: str, ds_id: int) -> pd.DataFrame:
    """
    Parse original Excel file and returns df in EnerMaps schema.

    Parameters
    ----------
    url : str
        Zenodo API url.

    ds_id : int

    Returns
    -------
    enermaps_data : pd.DataFrame
        Data in EnerMaps schema.

    """
    r = requests.get(url)
    if r.ok:
        metadata = r.json()
        for file in metadata["files"]:
            if file["key"] == DATASETS[ds_id]["file"]:
                filepath = file["links"]["self"]
                if not os.path.exists("{}".format(ds_id)):
                    logging.info("Downloading dataset {}".format(ds_id))
                    utilities.download_url(filepath, "{}.zip".format(ds_id))
                    extracted = utilities.extractZip(
                        "{}.zip".format(ds_id), "{}".format(ds_id)
                    )[0]
                logging.info(
                    "Loading dataset {}... (can take several minutes)".format(ds_id)
                )
                raw_data = pd.read_excel(extracted)
                os.remove("{}.zip".format(ds_id))
                shutil.rmtree("{}".format(ds_id))
                logging.info("Processing dataset {}".format(ds_id))
                # Create time series
                raw_data["start_at"] = pd.date_range(
                    START_DATE, periods=raw_data.shape[0], freq="H"
                )
                # Unpivot
                data = raw_data.melt(
                    id_vars=["start_at", DATASETS[ds_id]["time_variable"]],
                    var_name="fid",
                )

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
        enermaps_data["fid"] = data["fid"]
        enermaps_data["value"] = data["value"]
        enermaps_data["variable"] = DATASETS[ds_id]["variable"]
        enermaps_data["unit"] = DATASETS[ds_id]["unit"]
        enermaps_data["start_at"] = data["start_at"]
        enermaps_data["israster"] = ISRASTER

        return enermaps_data


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)
    for ds_id in ds_ids:
        data = get(url=datasets.loc[ds_id, "di_URL"], ds_id=ds_id)

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
        (
            metadata["parameters"],
            metadata["default_parameters"],
        ) = utilities.get_query_metadata(
            data, QUERY_FIELDS[ds_id], QUERY_PARAMETERS[ds_id]
        )
        metadata = json.dumps(metadata)
        dataset = pd.DataFrame([{"ds_id": ds_id, "metadata": metadata}])
        utilities.toPostgreSQL(
            dataset,
            DB_URL,
            schema="datasets",
        )

        # Create data table
        data["ds_id"] = ds_id
        utilities.toPostgreSQL(
            data,
            DB_URL,
            schema="data",
        )
