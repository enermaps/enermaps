#!/usr/bin/python
import json
import logging
import os
from datetime import datetime

import requests
from flask import current_app

from app.common import datasets, path
from app.models import storage

DATASETS_SERVER_URL = os.environ.get("DATASETS_SERVER_URL", "")
DATASETS_SERVER_API_KEY = os.environ.get("DATASETS_SERVER_API_KEY", "")
RASTER_SERVER_URL = os.environ.get("RASTER_SERVER_URL", "")


def get_dataset_list(disable_filtering=False, pretty_print=False):
    """Retrieve the list of all available datasets on the enermaps server"""
    url = DATASETS_SERVER_URL + "dataset_list"

    try:
        with requests.get(url) as resp:
            if pretty_print:
                _pretty_print_request(resp)

            datasets = resp.json()

        # If necessary: filter out datasets that don't exist in the cache
        if not (disable_filtering) and current_app.config["FILTER_DATASETS"]:
            datasets = [x for x in datasets if _dataset_is_on_disk(x)]

        return datasets

    except Exception as ex:
        logging.error(f"Failed to retrieve the list of datasets: {repr(ex)}")
        return []


def get_parameters(dataset_id, pretty_print=False):
    url = DATASETS_SERVER_URL + "rpc/enermaps_get_parameters"

    params = {
        "id": dataset_id,
    }

    headers = {"Authorization": "Bearer {}".format(DATASETS_SERVER_API_KEY)}

    try:
        with requests.get(url, headers=headers, params=params) as resp:
            if pretty_print:
                _pretty_print_request(resp)

            parameters = resp.json()

        return datasets.convert(parameters)

    except Exception as ex:
        logging.error(
            f"Failed to retrieve the variables of the dataset <{dataset_id}>: {repr(ex)}"
        )
        return None


def get_areas():
    """Return a list of all areas known by the platform"""
    return [
        {
            "id": "country",
            "title": "Countries",
        },
        {
            "id": "NUTS1",
            "title": "Region NUTS1",
        },
        {
            "id": "NUTS2",
            "title": "Region NUTS2",
        },
        {
            "id": "NUTS3",
            "title": "Region NUTS3",
        },
        {
            "id": "LAU",
            "title": "Cities",
        },
    ]


def get_geojson(layer_name, pretty_print=False):
    """
    Fetch a geojson dataset layer from the enermaps server with a given id.
    """
    parameters = _parameters_from_layer_name(layer_name)
    return _get_geojson(parameters, pretty_print)


def get_raster_file(dataset_id, feature_id):
    url = f"{RASTER_SERVER_URL}{dataset_id}/{feature_id}"

    try:
        with requests.get(url, stream=True) as resp:
            return resp.content
    except Exception as ex:
        logging.error(
            f"Failed to retrieve the raster file <{feature_id}> of dataset <{dataset_id}>: {repr(ex)}"
        )

    return None


def get_legend(layer_name, pretty_print=False):
    """
    Fetch a geojson dataset layer from the enermaps server with a given id.
    """
    url = DATASETS_SERVER_URL + "rpc/enermaps_get_legend"

    parameters = _parameters_from_layer_name(layer_name)

    headers = {"Authorization": "Bearer {}".format(DATASETS_SERVER_API_KEY)}

    try:
        params = {
            "parameters": json.dumps(parameters),
        }

        with requests.get(url, headers=headers, params=params) as resp:
            if pretty_print:
                _pretty_print_request(resp)

            return resp.json()
    except Exception as ex:
        logging.error(
            f"Failed to retrieve the legend of layer <{layer_name}>: {repr(ex)}"
        )

    return None


def get_area(id, pretty_print=False):
    """
    Fetch a geofile (geojson or raster) dataset layer from the enermaps server
    with a given Id.
    """
    parameters = {
        "data.ds_id": 0,
        "level": "{" + "{}".format(id) + "}",
    }

    return _get_geojson(parameters, pretty_print=pretty_print)


def _get_geojson(parameters, pretty_print=False):
    """
    Fetch a geofile (geojson or raster) dataset layer from the enermaps server
    with a given Id.
    """
    url = DATASETS_SERVER_URL + "rpc/enermaps_query_geojson"

    headers = {"Authorization": "Bearer {}".format(DATASETS_SERVER_API_KEY)}

    row_limit = 1000
    row_offset = 0
    all_data = None

    try:
        while True:
            params = {
                "parameters": json.dumps(parameters),
                "row_offset": row_offset,
                "row_limit": row_limit,
            }

            with requests.get(url, headers=headers, params=params) as resp:
                if pretty_print:
                    _pretty_print_request(resp)

                data = resp.json()

            if ("features" not in data) or (data["features"] is None):
                break

            if all_data is not None:
                all_data["features"].extend(data["features"])
            else:
                all_data = data

            if len(data["features"]) < row_limit:
                break

            row_offset += row_limit

    except Exception as ex:
        logging.error(f"Failed to retrieve the geojson: {repr(ex)}")
        return None

    return all_data


def _parameters_from_layer_name(layer_name):
    (type, id, variable, time_period, _) = path.parse_unique_layer_name(layer_name)

    parameters = {
        "data.ds_id": id,
    }

    dataset_parameters = get_parameters(id)
    datasets.process_parameters(dataset_parameters)

    if variable is not None:
        parameters["variable"] = f"'{variable}'"

    if time_period is not None:
        if time_period == str(None):
            parameters["start_at"] = None
        elif time_period.find("-") > 0:
            parameters["start_at"] = f"'{time_period}-01'"
        elif len(time_period) == 4:
            parameters["start_at"] = f"'{time_period}-01-01'"
        else:
            start = datetime.strptime(dataset_parameters["start_at"], "%Y-%m-%d %H:%M")
            parameters["start_at"] = f"'{start.year:04d}-{time_period}-01'"

    for k, v in dataset_parameters["default_parameters"].items():
        if k not in parameters:
            if k in ("fields", "intersecting"):
                parameters[k] = v
            elif k == "level":
                parameters[k] = f"{v}"
            else:
                parameters[k] = f"'{v}'"

    return parameters


def _dataset_is_on_disk(dataset):
    type = path.RASTER if dataset["is_raster"] else path.VECTOR
    dataset_name = path.make_unique_layer_name(type, dataset["ds_id"])
    storage_instance = storage.create_for_layer_type(type)
    return os.path.exists(storage_instance.get_dir(dataset_name))


def _pretty_print_request(response):
    print(
        "\n{}\n{}\n{}\n\n{}\n{}\n".format(
            "== Request ==========================",
            response.request.method + " " + response.request.url,
            "\r\n".join(
                "{}: {}".format(k, v) for k, v in response.request.headers.items()
            ),
            response.request.body,
            "=====================================",
        )
    )
