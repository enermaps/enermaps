#!/usr/bin/python
import io
import json
import logging
import os

import requests
from flask import current_app
from werkzeug.datastructures import FileStorage

from app.common import path
from app.data_integration import data_endpoints
from app.models import storage

DATASETS_SERVER_URL = os.environ.get("DATASETS_SERVER_URL", "")
DATASETS_SERVER_API_KEY = os.environ.get("DATASETS_SERVER_API_KEY", "")
RASTER_SERVER_URL = os.environ.get("RASTER_SERVER_URL", "")


def _dataset_is_on_disk(dataset):
    type = path.RASTER if dataset["is_raster"] else path.VECTOR
    dataset_name = path.make_unique_layer_name(type, dataset["ds_id"])
    storage_instance = storage.create_for_layer_type(type)
    return os.path.exists(storage_instance.get_dir(dataset_name))


def get_dataset_list(disable_filtering=False):
    """Retrieve the list of all available datasets on the enermaps server"""
    url = DATASETS_SERVER_URL + "dataset_list"

    try:
        with requests.get(url) as resp:
            datasets = resp.json()

        # If necessary: filter out datasets that don't exist in the cache
        if not (disable_filtering) and current_app.config["FILTER_DATASETS"]:
            datasets = [x for x in datasets if _dataset_is_on_disk(x)]

        return datasets

    except Exception as ex:
        logging.error(f"Failed to retrieve the list of datasets: {repr(ex)}")
        return []


def get_variables(dataset_id):
    url = DATASETS_SERVER_URL + "rpc/enermaps_get_variables"

    params = {
        "id": dataset_id,
    }

    headers = {"Authorization": "Bearer {}".format(DATASETS_SERVER_API_KEY)}

    try:
        with requests.get(url, headers=headers, params=params) as resp:
            variables = resp.json()

        # Ensure all fields have the format we want
        if ("variables" not in variables) or (variables["variables"] is None):
            variables["variables"] = []

        if ("time_periods" not in variables) or (variables["time_periods"] is None):
            variables["time_periods"] = []

        return variables

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


def get_nuts_and_lau_dataset(dataset_name):
    """
    Download NUTS and LAU geojson files from the enermaps server.
    Possible datasets names are: country, NUTS1, NUTS2, NUTS3, LAU
    """
    url = DATASETS_SERVER_URL + "rpc/enermaps_query_geojson"
    params = {
        "parameters": {
            "data.ds_id": "0",
            "level": "{" + "{}".format(dataset_name) + "}",
        },
        "row_limit": 100000,
    }
    try:
        headers = {"Authorization": "Bearer {}".format(DATASETS_SERVER_API_KEY)}
        with requests.post(url, headers=headers, json=params) as resp:
            # TODO check here that we have recieved a valid geojson?
            resp_data = io.BytesIO(resp.content)

        filename = "{}.geojson".format(dataset_name)
        content_type = "application/geo+json"
        file_upload = FileStorage(resp_data, filename, content_type=content_type)
        return file_upload
    except ConnectionError:
        raise


def get_geojson(layer_name):
    """
    Fetch a geofile (geojson or raster) dataset layer from the enermaps server
    with a given Id.
    """
    (type, id, variable, time_period) = path.parse_unique_layer_name(layer_name)

    parameters = {
        "data.ds_id": id,
    }

    if variable is not None:
        parameters["variable"] = f"'{variable}'"

    if time_period is not None:
        parameters["start_at"] = f"'{time_period}-01-01'"

    return _get_geojson(parameters)


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


def get_area(id):
    """
    Fetch a geofile (geojson or raster) dataset layer from the enermaps server
    with a given Id.
    """
    parameters = {
        "data.ds_id": 0,
        "level": "{" + "{}".format(id) + "}",
    }

    return _get_geojson(parameters)


def _get_geojson(parameters):
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
                data = resp.json()

            if data["features"] is None:
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


def get_dataset(dataset_id):
    """
    Fetch a geofile (geojson or raster) dataset layer from the enermaps server
    with a given Id.
    """
    url = DATASETS_SERVER_URL + "rpc/enermaps_query_geojson"

    # All the parameters needed to fetch (one layer of) the dataset are obtained
    # from the configuration file
    params = data_endpoints.get_json_params(dataset_id)
    layer_type, _ = data_endpoints.get_ds_type(dataset_id)
    dataset_title = data_endpoints.get_ds_title(dataset_id)

    # If the layer is a vector layer, it is converted into a FileStorage instance
    if (params is not None) and (layer_type == "vector"):
        try:
            headers = {"Authorization": "Bearer {}".format(DATASETS_SERVER_API_KEY)}
            with requests.post(url, headers=headers, json=params) as resp:
                # TODO check here that we have recieved a valid geojson?
                geojson = resp.json()
                with open("data.json", "w") as f:
                    json.dump(geojson, f, indent=4)
                for i in range(len(geojson["features"])):
                    # Modify the original geojson to put the legend key some levels higher
                    # (needed by mapnik to make the color rules)
                    legend_variable = data_endpoints.get_legend_variable(dataset_id)
                    if isinstance(legend_variable, dict):
                        geojson["features"][i]["properties"]["legend"] = geojson[
                            "features"
                        ][i]["properties"]["variables"][legend_variable["variable"]]

                resp_data = io.BytesIO(
                    json.dumps(geojson, indent=4, sort_keys=True).encode("utf8")
                )

            filename = "{:02d}_{}.geojson".format(dataset_id, dataset_title)
            content_type = "application/geo+json"
            file_upload = FileStorage(resp_data, filename, content_type=content_type)
            return file_upload
        except ConnectionError:
            raise

    # If the layer is a raster file, we need to read the name of the raster file wich is
    # contained in the geojson, reconstruct the address of the raster file and download
    # the raster at this address.
    # Finally, we create a FileStorage instance.
    if (params is not None) and (layer_type == "raster"):
        # We need to get the dataset info from the db before downloading the files
        # on another server
        file_name = None
        try:
            headers = {"Authorization": "Bearer {}".format(DATASETS_SERVER_API_KEY)}
            with requests.post(url, headers=headers, json=params) as resp:
                resp_data = resp.json()

                # If there is multiple images to download, download only the 1st one
                # TODO download all the images and combine them - How???
                file_name = resp_data["features"][0]["id"]

            # Create the url to download the file
            # TODO check extension to be sure we have an image
            raster_url = RASTER_SERVER_URL + str(dataset_id) + "/" + file_name
            try:
                with requests.get(raster_url, stream=True) as resp:
                    resp_data = io.BytesIO(resp.content)
            except ConnectionError:
                raise

            storage_filename = "{:02d}_{}.tiff".format(dataset_id, dataset_title)
            content_type = "image/tiff"
            file_upload = FileStorage(
                resp_data, storage_filename, content_type=content_type
            )
            return file_upload

        except Exception:
            raise
