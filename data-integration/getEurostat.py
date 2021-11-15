#!/usr/bin/env python3
"""
Retrieve datasets from Eurostat.
Allow for updates without checking metadata.

@author: giuseppeperonato
"""
import json
import logging
import os
import sys

import pandas as pd
import pandasdmx as sdmx
import requests
import utilities

# Constants
logging.basicConfig(level=logging.INFO)
ISRASTER = False
TRANSL = {"EL": "GR", "UK": "GB"}

QUERIES = {
    6: dict(
        provider="ESTAT",
        stat_id="nrg_d_hhq",
        dimensions=["SIEC", "NRG_BAL"],
        filters={"UNIT": "GWH"},
    ),
    9: dict(
        provider="ESTAT",
        stat_id="nrg_chddr2_m",
        dimensions=["INDIC_NRG"],
        filters={"UNIT": "NR"},
        parameters={"startPeriod": 1970, "endPeriod": pd.Timestamp.today().year},
    ),
    22: dict(
        provider="ESTAT",
        stat_id="nrg_ind_eff",
        dimensions=["NRG_BAL"],
        filters={"UNIT": "MTOE"},
    ),
    42: dict(
        provider="ESTAT", stat_id="cens_11dwob_r3", dimensions=["BUILDING", "HOUSING"]
    ),
    47: dict(
        provider="ESTAT",
        stat_id="nrg_pc_204",
        dimensions=["CONSOM", "TAX"],
        filters={"UNIT": "KWH", "CURRENCY": "EUR"},
    ),
    48: dict(
        provider="ESTAT",
        stat_id="nama_10_co3_p3",
        dimensions=["COICOP"],
        filters={"UNIT": "CP_MEUR", "COICOP": "CP045"},
    ),
    49: dict(
        provider="ESTAT",
        stat_id="t2020_rd320",
        dimensions=["SIEC"],
        filters={"UNIT": "PC"},
    ),
    50: dict(provider="ESTAT", stat_id="tgs00004", dimensions=[], filters={}),
}

QUERY_FIELDS = {
    6: dict(
        [],
    ),  # empty list means all; None means do not use query fields.
    9: dict(
        [],
    ),  # empty list means all; None means do not use query fields.
    22: dict(
        [],
    ),  # empty list means all; None means do not use query fields.
    42: dict(
        [],
    ),  # empty list means all; None means do not use query fields.
    47: dict(
        [],
    ),  # empty list means all; None means do not use query fields.
    48: dict(
        [],
    ),  # empty list means all; None means do not use query fields.
    49: dict(
        [],
    ),  # empty list means all; None means do not use query fields.
    50: dict(
        [],
    ),  # empty list means all; None means do not use query fields.
}

QUERY_PARAMETERS = {
    6: {"temporal_granularity": "year", "is_tiled": False, "is_raster": False},
    9: {
        "temporal_granularity": "month",
        "is_tiled": False,
        "is_raster": False,
        "levels": ["NUTS3", "NUTS2", "NUTS1", "country"],
    },
    22: {"temporal_granularity": "year", "is_tiled": False, "is_raster": False},
    42: {
        "temporal_granularity": "custom",
        "is_tiled": False,
        "is_raster": False,
        "levels": ["NUTS3", "NUTS2", "NUTS1", "country"],
    },
    47: {"temporal_granularity": "semester", "is_tiled": False, "is_raster": False},
    48: {"temporal_granularity": "year", "is_tiled": False, "is_raster": False},
    49: {"temporal_granularity": "year", "is_tiled": False, "is_raster": False},
    50: {"temporal_granularity": "year", "is_tiled": False, "is_raster": False},
}


DB_URL = utilities.DB_URL


def get(provider, stat_id, dimensions=[], filters={}, parameters={}):
    """
    Query Euostat database.

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
    stat = sdmx.Request(provider)
    metadata = stat.datastructure("DSD_{}".format(stat_id))

    if len(filters) > 0:
        if len(parameters) > 0:
            dfs = []
            for year in range(
                int(parameters["startPeriod"]), int(parameters["endPeriod"]) + 1
            ):
                logging.info("Retrieving year {}".format(year))
                resp = stat.data(
                    stat_id,
                    key=filters,
                    params={"startPeriod": str(year), "endPeriod": str(year)},
                )
                data = resp.to_pandas()
                if len(data) > 0:
                    dfs.append(data)
            data = pd.concat(dfs, axis=0)
        else:
            resp = stat.data(stat_id, key=filters)
            data = resp.to_pandas()
    else:
        try:
            resp = stat.data(stat_id)
            data = resp.to_pandas()
        except requests.exceptions.HTTPError as e:
            print(e)
    if len(data) > 0:
        # Remove multi-index
        data = data.reset_index()

        # Translate codes to names using metadata codelist
        data_transl = data.copy()
        if provider == "OECD":
            pass
        else:
            for key in metadata.codelist.keys():
                column = key.replace("CL_", "")
                if column != "GEO":
                    try:
                        data_transl[column] = data_transl[column].replace(
                            sdmx.to_pandas(metadata.codelist[key]).to_dict()
                        )
                    except KeyError:
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
        enermaps_data["israster"] = ISRASTER

        # Country codes to ISO-3166
        enermaps_data["fid"] = enermaps_data["fid"].replace(TRANSL)

        return enermaps_data
    else:
        logging.error("No data returned.")
        return None


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)
    for ds_id in ds_ids:
        logging.info(
            "{} - {}".format(ds_id, datasets.loc[ds_id, "Title"])
        )

        if utilities.datasetExists(
            ds_id,
            DB_URL,
        ):
            if isForced:
                utilities.removeDataset(ds_id, DB_URL)
                logging.info("Removed existing dataset")
            else:
                logging.error("Dataset already existing. Use --force to replace it.")

        if not utilities.datasetExists(
            ds_id,
            DB_URL,
        ):
            data = get(**QUERIES[ds_id])
            metadata = datasets.loc[ds_id].fillna("").to_dict()
            # Add parameters as metadata
            (
                metadata["parameters"],
                metadata["default_parameters"],
            ) = utilities.get_query_metadata(
                data, QUERY_FIELDS[ds_id], QUERY_PARAMETERS[ds_id]
            )
            metadata = json.dumps(metadata)
            dataset = pd.DataFrame(
                [
                    {
                        "ds_id": ds_id,
                        "metadata": metadata,
                        "shared_id": datasets.loc[ds_id, "shared_id"],
                    }
                ]
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
