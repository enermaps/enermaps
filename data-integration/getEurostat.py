#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 11:02:20 2021

@author: giuseppeperonato
"""
import argparse
import pandas as pd
import logging
import pandasdmx as sdmx
import utilities
import json
import sys
import os

# Constants
logging.basicConfig(level=logging.INFO)

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

QUERIES = {
    6: dict(
        eurostat_id="nrg_d_hhq",
        dimensions=["SIEC", "NRG_BAL"],
        filters={"UNIT": "GWH"},
    ),
    9: dict(
        eurostat_id="nrg_chdd_a", dimensions=["INDIC_NRG"], filters={"UNIT": "NR"}
    ),
    22: dict(
        eurostat_id="nrg_chdd_a", dimensions=["INDIC_NRG"], filters={"UNIT": "NR"}
    ),
    47: dict(
        eurostat_id="nrg_pc_204",
        dimensions=["CONSOM", "TAX"],
        filters={"UNIT": "KWH", "CURRENCY": "EUR"},
    ),
    48: dict(
        eurostat_id="nama_10_co3_p3",
        dimensions=["COICOP"],
        filters={"UNIT": "CP_MEUR", "COICOP": "CP045"},
    ),
    49: dict(
        eurostat_id="t2020_rd320", dimensions=["SIEC"], filters={"UNIT": "PC"}
    ),
    50: dict(eurostat_id="tgs00004", dimensions=[], filters={}),
}

def get(eurostat_id, dimensions=[], filters={}):
    """
    Queries Euostat database

    Parameters
    ----------
    eurostat_id : str
        DESCRIPTION.
    dimensions : list of string, optional
        DESCRIPTION. Select dimensions to aggregate as variable name. The default is [].
    filters : dictionary, optional
        DESCRIPTION. Limit the queries to some values. The default is {}.

    Returns
    -------
    enermaps_data : DataFrame
        Data value following Enermaps schema.

    """
    estat = sdmx.Request("ESTAT")
    metadata = estat.datastructure("DSD_{}".format(eurostat_id))

    if len(filters) > 0:
        resp = estat.data(
            eurostat_id,
            key=filters
            # params={'startPeriod': '2007'},
        )
    else:
        resp = estat.data(
            eurostat_id,
            # key=filters
            # params={'startPeriod': '2007'},
        )
    data = resp.to_pandas()

    # Remove multi-index
    data = data.reset_index()

    # Translate codes to names using metadata codelist
    data_transl = data.copy()
    for key in metadata.codelist.keys():
        column = key.replace("CL_", "")
        if column != "GEO":
            try:
                data_transl[column] = data_transl[column].replace(
                    sdmx.to_pandas(metadata.codelist[key]).to_dict()
                )
            except:
                pass

    # Remove lines with no values
    data_transl = data_transl.dropna()

    # Translate frequency to hours
    if "FREQ" in data_transl.columns:
        freq = {
            "Daily": 24,
            "Weekly": 168,
            "Quarterly": 2190,
            "Annual": 8760,
            "Semi-annual": 4380,
            "Monthly": 730,
            "Half-year": 4380,
        }
        data_transl["FREQ"] = data_transl["FREQ"].replace(freq)
        # Translate biannual strings to dates
        data_transl["TIME_PERIOD"] = data_transl["TIME_PERIOD"].str.replace(
            "B1", "01-01"
        )
        data_transl["TIME_PERIOD"] = data_transl["TIME_PERIOD"].str.replace(
            "B2", "07-01"
        )

    # Create final EnerMaps data table
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
        ]
    )

    # Attribute the fields that remain the same
    enermaps_data[["start_at", "dt", "fid", "unit", "value"]] = data_transl[
        ["TIME_PERIOD", "FREQ", "GEO", "UNIT", "value"]
    ]

    # Aggregate the dimensions into a single variable
    if len(dimensions) > 0:
        enermaps_data["variable"] = data_transl[dimensions].agg(" : ".join, axis=1)
    else:
        enermaps_data["variable"] = "default"


    # Year to datetime
    enermaps_data["start_at"] = pd.to_datetime(enermaps_data["start_at"])

    return enermaps_data


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_ids = QUERIES.keys()
    isForced = False
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Import Eurostat")
        parser.add_argument("--force", action="store_const", const=True, default=False)
        parser.add_argument(
            "--select_ds_ids", action="extend", nargs="+", type=int, default=[]
        )
        args = parser.parse_args()
        isForced = args.force
        if len(args.select_ds_ids) > 0:
            ds_ids = args.select_ds_ids
        

    for ds_id in ds_ids:
        logging.info("Processing ds {} - {}".format(ds_id, datasets.loc[ds_id,"Title (with Hyperlink)"]))

        if utilities.datasetExists(ds_id, DB_URL,):
                if isForced:
                    utilities.removeDataset(ds_id, DB_URL)
                    logging.info("Removed existing dataset")
                else:
                    logging.error("Dataset already existing. Use --force to replace it.")
        
        print("Processing ds {} - {}".format(ds_id, datasets.loc[ds_id].iloc[2]))
        data = get(**QUERIES[ds_id])

        dataset = pd.DataFrame(
            [{"ds_id": ds_id, "metadata": datasets.loc[ds_id].to_json()}]
        )
        utilities.toPostgreSQL(
            dataset,
            DB_URL,
            schema="datasets",
        )

        data["ds_id"] = ds_id
        data["israster"] = False
        utilities.toPostgreSQL(
            data,
            DB_URL,
            schema="data",
        )
