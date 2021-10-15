import itertools
import json
import time

import click
from flask import current_app
from flask.cli import with_appcontext

from app.common import path
from app.data_integration import enermaps_server as client
from app.models import geofile


@click.command("update-all-datasets")
@with_appcontext
def update_all_datasets():
    datasets = client.get_dataset_list(disable_filtering=True)
    for dataset in datasets:
        process_dataset(dataset)


@click.command("update-dataset")
@click.argument("ds_id")
@with_appcontext
def update_dataset(ds_id):
    datasets = client.get_dataset_list(disable_filtering=True)
    datasets = [x for x in datasets if x["ds_id"] == int(ds_id)]

    if len(datasets) == 1:
        process_dataset(datasets[0])


@click.command("update-areas")
@with_appcontext
def update_areas():
    areas = client.get_areas()
    for area in areas:
        process_area(area["id"])


@click.command("list-datasets")
@with_appcontext
def list_datasets():
    datasets = client.get_dataset_list(disable_filtering=True)

    result = "\n"

    for dataset in datasets:
        type = "raster" if dataset["is_raster"] else "vector"
        result += f"- {dataset['ds_id']}: {dataset['title']} ({type})\n"

    current_app.logger.info(result)


@click.command("list-variables")
@click.argument("ds_id")
@with_appcontext
def list_variables(ds_id):
    datasets = client.get_dataset_list(disable_filtering=True)
    datasets = [x for x in datasets if x["ds_id"] == int(ds_id)]

    if len(datasets) == 1:
        variables = client.get_variables(datasets[0]["ds_id"])

        result = "\n"

        if len(variables["variables"]) > 0:
            result += "Variables:\n"
            for variable in variables["variables"]:
                result += f"- {variable}\n"

        if len(variables["time_periods"]) > 0:
            if result == "\n":
                result += "\n"

            result += "Time periods:\n"
            for time_period in variables["time_periods"]:
                result += f"- {time_period}\n"

        if result == "\n":
            result += "No variable nor time period"

        current_app.logger.info(result)


@click.command("get-legend")
@click.argument("ds_id")
@click.argument("variable")
@click.argument("time_period")
@with_appcontext
def get_legend(ds_id, variable, time_period):
    if variable == "-":
        variable = None

    if time_period == "-":
        time_period = None

    datasets = client.get_dataset_list(disable_filtering=True)
    datasets = [x for x in datasets if x["ds_id"] == int(ds_id)]

    if len(datasets) == 1:
        dataset = datasets[0]

        type = "raster" if dataset["is_raster"] else "vector"
        layer_name = path.make_unique_layer_name(
            type, ds_id, variable=variable, time_period=time_period
        )

        legend = client.get_legend(layer_name)

        result = "\n"
        result += json.dumps(legend, indent=4)

        current_app.logger.info(result)


def process_dataset(dataset):
    type = path.RASTER if dataset["is_raster"] else path.VECTOR

    # Retrieve the variables of the dataset
    variables = client.get_variables(dataset["ds_id"])

    # For vector datasets, we want to retrieve all variables at once
    if type == path.VECTOR:
        variables["variables"] = []

    # Iterate over all combinations of variables and time_periods
    if (len(variables["variables"]) > 0) and (len(variables["time_periods"]) > 0):
        for variable, time_period in itertools.product(
            variables["variables"], variables["time_periods"]
        ):
            process_layer(
                type, dataset["ds_id"], variable=variable, time_period=time_period
            )
    elif len(variables["variables"]) > 0:
        for variable in variables["variables"]:
            process_layer(type, dataset["ds_id"], variable=variable)
    elif len(variables["time_periods"]) > 0:
        for time_period in variables["time_periods"]:
            process_layer(type, dataset["ds_id"], time_period=time_period)
    else:
        process_layer(type, dataset["ds_id"])


def process_layer(type, id, variable=None, time_period=None):
    layer_name = path.make_unique_layer_name(
        type, id, variable=variable, time_period=time_period
    )

    current_app.logger.info(f"Download geojson <{layer_name}>...")

    time_started = time.time()
    data = client.get_geojson(layer_name)
    time_fetched = time.time()

    current_app.logger.info(
        f"... fetch done in {int(time_fetched - time_started)} seconds"
    )

    if type == path.VECTOR:
        geofile.save_vector_geojson(layer_name, data)
    else:
        for feature in data["features"]:
            feature_id = feature["id"]
            current_app.logger.info(f"... download raster file <{feature_id}>")
            raster_content = client.get_raster_file(id, feature_id)
            if raster_content is not None:
                geofile.save_raster_file(layer_name, feature_id, raster_content)

    time_saved = time.time()
    current_app.logger.info(
        f"... save done in {int(time_saved - time_fetched)} seconds."
    )


def process_area(id):
    layer_name = path.make_unique_layer_name(path.AREA, id)

    current_app.logger.info(f"Download area <{id}>...")

    time_started = time.time()
    data = client.get_area(id)
    time_fetched = time.time()

    current_app.logger.info(
        f"... fetch done in {int(time_fetched - time_started)} seconds"
    )

    geofile.save_vector_geojson(layer_name, data)

    time_saved = time.time()
    current_app.logger.info(
        f"... save done in {int(time_saved - time_fetched)} seconds."
    )
