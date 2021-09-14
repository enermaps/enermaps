#!/usr/bin/env python3
"""
Get Electricity capacity from electricitymap.org JSON.

Allow updates only if validation of json schema is obtained.
Store metadata in a non-standard datapackage.

@author: giuseppeperonato
"""

import json
import logging
import os
import sys
from typing import Union

import jsonschema
import pandas as pd
import requests
import utilities
from jsonschema.exceptions import ValidationError

OTHER_FIELDS = ["contributors", "delays", "comment"]
UNITS = "MW"
VARIABLE = "Electricity production capacity"
ISRASTER = False

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "$id": "https://github.com/tmrowco/electricitymap-contrib/blob/master/config/zones.schema.json",
    "title": "ElectricityMap Zones",
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "_todo": {"type": "string"},
            "_comment": {"type": "string"},
            "comment": {"type": "string"},
            "flag_file_name": {"type": "string"},
            "bounding_box": {
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {"type": "number", "minItems": 2, "maxItems": 2},
                },
            },
            "capacity": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "battery storage": {"type": "number", "minimum": 0},
                    "biomass": {"type": "number", "minimum": 0},
                    "coal": {"type": "number", "minimum": 0},
                    "gas": {"type": "number", "minimum": 0},
                    "geothermal": {"type": "number", "minimum": 0},
                    "hydro": {"type": "number", "minimum": 0},
                    "hydro storage": {"type": "number", "minimum": 0},
                    "nuclear": {"type": "number", "minimum": 0},
                    "oil": {"type": "number", "minimum": 0},
                    "solar": {"type": "number", "minimum": 0},
                    "unknown": {"type": "number", "minimum": 0},
                    "wind": {"type": "number", "minimum": 0},
                },
            },
            "contributors": {"type": "array", "items": {"type": "string"}},
            "disclaimer": {"type": "string"},
            "parsers": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "consumption": {"type": "string"},
                    "consumptionForecast": {"type": "string"},
                    "generationForecast": {"type": "string"},
                    "productionPerModeForecast": {"type": "string"},
                    "price": {"type": "string"},
                    "production": {"type": "string"},
                    "productionPerUnit": {"type": "string"},
                },
            },
            "subZoneNames": {"type": "array", "items": {"type": "string"}},
            "delays": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "production": {"type": "number", "minimum": 0},
                    "consumptionForecast": {"type": "number", "minimum": 0},
                    "consumption": {"type": "number", "minimum": 0},
                },
            },
            "timezone": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        },
    },
}

SOURCES = SCHEMA["additionalProperties"]["properties"]["capacity"]["properties"].keys()

logging.basicConfig(level=logging.INFO)

DB_URL = utilities.DB_URL


def isValid(dp: dict(), new_dp: dict()) -> bool:
    """Check whether the new DataPackage is valid and make sure the schema has not changed."""
    # Validate the new instance against the old schema
    valid = True  # initialize
    try:
        jsonschema.validate(
            instance=requests.get(new_dp["url"]).json(), schema=dp["schema"]
        )
    except ValidationError:
        valid = False
    if dp["schema"] == new_dp["schema"] and valid:
        logging.info("Returning valid and schema-compliant data")
        return True
    else:
        logging.error("Data is not valid or the schema has changed")
        return False


def prepare(dp: dict) -> pd.DataFrame:
    """Prepare data in EnerMaps format."""
    zones = requests.get(dp["url"]).json()
    sources = []
    locations = []
    other_fields = []
    for zone in zones:
        if zones[zone].get("capacity"):
            sources.append(zones[zone].get("capacity"))
            locations.append(zone)
            fields = {}
            # Keep only known other fields
            for field in OTHER_FIELDS:
                if field in zones[zone].keys():
                    fields[field] = zones[zone][field]
            other_fields.append(fields)
    # Keep only known sources by forcing the df columns
    data = pd.DataFrame(sources, columns=SOURCES)
    data["fid"] = locations
    data["fields"] = other_fields

    # Unpivot
    data = data.melt(id_vars=["fields", "fid"])

    # Add unpivoted energy source as field
    data["fields"] = data.apply(
        lambda x: json.dumps({**x["fields"], "Energy source": x["variable"]}), axis=1
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
    enermaps_data["variable"] = VARIABLE
    enermaps_data["fields"] = data["fields"]
    enermaps_data["unit"] = UNITS
    enermaps_data["israster"] = ISRASTER

    return enermaps_data


def get(url: str, dp: dict, force: bool) -> Union[pd.DataFrame, dict]:
    """Obtain metadata and data."""
    user, repo, branch = url.split("/")[3:6]
    file = "/".join(url.split("/")[-2:])

    # Create (non-standard) datapackage with minimun metadata
    new_dp = {}
    new_dp["url"] = url
    new_dp["datePublished"] = utilities.getGitHub(user, repo, "date", file, branch)
    new_dp["schema"] = SCHEMA

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        if "datePublished" in dp.keys():
            isChangedDate = dp["datePublished"] != new_dp["datePublished"]
        else:
            isChangedDate = False
        if (
            isChangedDate
        ):  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            if isValid(dp, new_dp):
                enermaps_data = prepare(new_dp)
            else:
                return None, None
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            if isValid(dp, new_dp):
                enermaps_data = prepare(new_dp)
            else:
                return None, None
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None
    else:  # New dataset
        dp = new_dp  # this is just for the sake of the schema control
        if isValid(dp, new_dp):
            enermaps_data = prepare(new_dp)
        else:
            return None, None

    return enermaps_data, new_dp


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)

    for ds_id in ds_ids:
        url = datasets.loc[ds_id, "di_URL"]
        dp = utilities.getDataPackage(ds_id, DB_URL)

        data, dp = get(url=url, dp=dp, force=isForced)

        if isinstance(data, pd.DataFrame):
            # Remove existing dataset
            if utilities.datasetExists(ds_id, DB_URL,):
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
            utilities.toPostgreSQL(data, DB_URL, schema="data")
