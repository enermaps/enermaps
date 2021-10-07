import itertools
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


def process_dataset(dataset):
    type = path.RASTER if dataset["is_raster"] else path.VECTOR

    # Retrieve the variables of the dataset
    variables = client.get_variables(dataset["ds_id"])

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
