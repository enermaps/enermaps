import itertools
import json
import time

import click
from flask import current_app
from flask.cli import with_appcontext

from app.common import client
from app.common import datasets as datasets_fcts
from app.common import path
from app.common.projection import epsg_string_to_proj4
from app.models import geofile, storage


@click.command("update-all-datasets")
@with_appcontext
def update_all_datasets():
    datasets = client.get_dataset_list(disable_filtering=True)
    if len(datasets) == 0:
        current_app.logger.info("No dataset found")
        return

    for dataset in datasets:
        process_dataset(dataset, ignore_intersecting=True)


@click.command("update-dataset")
@click.argument("ds_id")
@click.option("--all", is_flag=True)
@click.option("-p", "--prettyprint", is_flag=True)
@with_appcontext
def update_dataset(ds_id, all, prettyprint):
    datasets = client.get_dataset_list(disable_filtering=True)
    datasets = [x for x in datasets if x["ds_id"] == int(ds_id)]

    if len(datasets) == 1:
        process_dataset(datasets[0], ignore_intersecting=all, pretty_print=prettyprint)
    else:
        current_app.logger.info("Dataset not found")


@click.command("update-areas")
@with_appcontext
def update_areas():
    areas = client.get_areas()
    if len(areas) == 0:
        current_app.logger.info("No area found")

    for area in areas:
        process_area(area["id"])


@click.command("list-datasets")
@click.option("-p", "--prettyprint", is_flag=True)
@with_appcontext
def list_datasets(prettyprint):
    datasets = client.get_dataset_list(disable_filtering=True, pretty_print=prettyprint)
    if len(datasets) == 0:
        current_app.logger.info("No dataset found")
        return

    result = "\n"

    for dataset in datasets:
        type = "raster" if dataset["is_raster"] else "vector"
        result += f"- {dataset['ds_id']}: {dataset['title']} ({type})\n"

    current_app.logger.info(result)


@click.command("get-parameters")
@click.argument("ds_id")
@click.option("--processing", is_flag=True)
@click.option("-p", "--prettyprint", is_flag=True)
@with_appcontext
def get_parameters(ds_id, processing, prettyprint):
    def _process_list(result, parameters, name, label):
        if len(parameters[name]) > 0:
            if result != "\n":
                result += "\n"

            result += f"{label}:\n"
            for value in parameters[name]:
                result += f"- {value}\n"

        return result

    def _process_dict(result, parameters, name, label):
        if len(parameters[name]) > 0:
            if result != "\n":
                result += "\n"

            result += f"{label}:\n"
            for key, value in parameters[name].items():
                result += f"- {key}: {value}\n"

        return result

    def _process_variable(result, parameters, name, label):
        if parameters[name] is not None:
            if result != "\n":
                result += "\n"

            result += f"{label}: {parameters[name]}\n"

        return result

    def _display_parameters(result, parameters):
        result = _process_list(result, parameters, "variables", "Variables")
        result = _process_list(result, parameters, "time_periods", "Time periods")
        result = _process_dict(result, parameters, "fields", "Fields")
        result = _process_list(result, parameters, "levels", "Levels")
        result = _process_variable(
            result, parameters, "temporal_granularity", "Temporal granularity"
        )
        result = _process_variable(result, parameters, "start_at", "Start date")
        result = _process_variable(result, parameters, "end_at", "End date")
        result = _process_dict(
            result, parameters, "default_parameters", "Default parameters"
        )
        return result

    datasets = client.get_dataset_list(disable_filtering=True)
    datasets = [x for x in datasets if x["ds_id"] == int(ds_id)]

    if len(datasets) == 1:
        parameters = client.get_parameters(
            datasets[0]["ds_id"], pretty_print=prettyprint
        )

        if parameters is None:
            current_app.logger.info("Failed to retrieve the parameters")
            return

        result = "\n"
        result = _display_parameters(result, parameters)

        if result == "\n":
            result += "No variable nor time period"
        elif processing:
            result += "\n------------->\n"
            datasets_fcts.process_parameters(parameters)
            result = _display_parameters(result, parameters)

        current_app.logger.info(result)
    else:
        current_app.logger.info("Dataset not found")
        return


@click.command("get-legend")
@click.argument("ds_id")
@click.option("-v", "--variable", default=None)
@click.option("-t", "--time_period", default=None)
@click.option("-p", "--prettyprint", is_flag=True)
@with_appcontext
def get_legend(ds_id, variable, time_period, prettyprint):
    datasets = client.get_dataset_list(disable_filtering=True)
    datasets = [x for x in datasets if x["ds_id"] == int(ds_id)]

    if len(datasets) == 1:
        dataset = datasets[0]

        type = "raster" if dataset["is_raster"] else "vector"
        layer_name = path.make_unique_layer_name(
            type, ds_id, variable=variable, time_period=time_period
        )

        legend = client.get_legend(layer_name, pretty_print=prettyprint)
        if legend is None:
            current_app.logger.info("Failed to retrieve the legend")
            return

        result = "\n"
        result += json.dumps(legend, indent=4)

        current_app.logger.info(result)
    else:
        current_app.logger.info("Dataset not found")
        return


def process_dataset(dataset, ignore_intersecting=False, pretty_print=False):
    type = path.RASTER if dataset["is_raster"] else path.VECTOR

    # Retrieve the variables of the dataset
    parameters = client.get_parameters(dataset["ds_id"])
    if parameters is None:
        return

    datasets_fcts.process_parameters(parameters)

    # For vector datasets, we want to retrieve all variables at once
    if type == path.VECTOR:
        parameters["variables"] = []

    # Iterate over all combinations of variables and time_periods
    if (len(parameters["variables"]) > 0) and (len(parameters["time_periods"]) > 0):
        for variable, time_period in itertools.product(
            parameters["variables"], parameters["time_periods"]
        ):
            success, _ = process_layer(
                type,
                dataset["ds_id"],
                variable=variable,
                time_period=time_period,
                ignore_intersecting=ignore_intersecting,
                pretty_print=pretty_print,
            )

            if not success:
                break

    elif len(parameters["variables"]) > 0:
        for variable in parameters["variables"]:
            success, _ = process_layer(
                type,
                dataset["ds_id"],
                variable=variable,
                ignore_intersecting=ignore_intersecting,
                pretty_print=pretty_print,
            )

            if not success:
                break
    elif len(parameters["time_periods"]) > 0:
        valid_combinations = {}

        for time_period in parameters["time_periods"]:
            success, valid_variables = process_layer(
                type,
                dataset["ds_id"],
                time_period=time_period,
                ignore_intersecting=ignore_intersecting,
                pretty_print=pretty_print,
            )

            if not success:
                break

            if valid_variables is not None:
                if time_period not in valid_combinations:
                    valid_combinations[time_period] = []

                valid_combinations[time_period].extend(valid_variables)

        if (type == path.VECTOR) and (len(valid_combinations) > 0):
            layer_name = path.make_unique_layer_name(type, dataset["ds_id"])
            storage_instance = storage.create(layer_name)
            with open(
                storage_instance.get_combinations_file(layer_name),
                "w",
            ) as f:
                json.dump(valid_combinations, f)
    else:
        success, _ = process_layer(
            type,
            dataset["ds_id"],
            ignore_intersecting=ignore_intersecting,
            pretty_print=pretty_print,
        )

    # For raster datasets, save the projection in a file
    if success and (type == path.RASTER):
        current_app.logger.info("... save projection")
        layer_name = path.make_unique_layer_name(type, dataset["ds_id"])
        geofile.save_raster_projection(
            layer_name,
            epsg_string_to_proj4(current_app.config["RASTER_PROJECTION_SYSTEM"]),
        )


def process_layer(
    type,
    id,
    variable=None,
    time_period=None,
    ignore_intersecting=False,
    pretty_print=False,
):
    layer_name = path.make_unique_layer_name(
        type, id, variable=variable, time_period=time_period
    )

    current_app.logger.info(f"Download geojson <{layer_name}>...")

    time_started = time.time()

    data = client.get_geojson(
        layer_name, ignore_intersecting=ignore_intersecting, pretty_print=pretty_print
    )

    if data is None:
        current_app.logger.info("... failed to retrieve the geojson")
        return (False, None)

    if (data["features"] is None) or (len(data["features"]) == 0):
        current_app.logger.info("... no feature found in the geojson")
        return (False, None)

    time_fetched = time.time()

    current_app.logger.info(
        f"... fetch done in {int(time_fetched - time_started)} seconds"
    )

    geofile.delete_all_features(layer_name)

    valid_variables = None
    success = True

    if type == path.VECTOR:
        valid_variables = geofile.save_vector_geojson(layer_name, data)
    else:
        # Don't download raster files if we have directly access to them
        if current_app.config["RASTER_CACHE_DIR"] is None:
            for feature in data["features"]:
                feature_id = feature["id"]
                current_app.logger.info(f"... download raster file <{feature_id}>")
                raster_content = client.get_raster_file(id, feature_id)

                if raster_content is not None:
                    geofile.save_raster_file(layer_name, feature_id, raster_content)
                else:
                    success = False
                    break

        current_app.logger.info("... save geometries")
        geofile.save_raster_geometries(layer_name, data)

    time_saved = time.time()
    current_app.logger.info(
        f"... save done in {int(time_saved - time_fetched)} seconds."
    )

    return (success, valid_variables)


def process_area(id):
    layer_name = path.make_unique_layer_name(path.AREA, id)

    current_app.logger.info(f"Download area <{id}>...")

    time_started = time.time()
    data = client.get_area(id)
    if data is None:
        return

    time_fetched = time.time()

    current_app.logger.info(
        f"... fetch done in {int(time_fetched - time_started)} seconds"
    )

    geofile.save_vector_geojson(layer_name, data)

    time_saved = time.time()
    current_app.logger.info(
        f"... save done in {int(time_saved - time_fetched)} seconds."
    )
