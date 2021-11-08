"""Endpoint for the manipulation of datasets
"""

import hashlib

from flask import Response
from flask_restx import Namespace, Resource, abort

from app.common import client
from app.common import datasets as datasets_fcts
from app.common import path

api = Namespace("datasets", description="Datasets related endpoints")


@api.route("/")
class Datasets(Resource):
    def get(self):
        """Return a list of all datasets known by the platform"""
        datasets = client.get_dataset_list()
        if len(datasets) == 0:
            abort(404)

        add_openaire_links(datasets)

        return datasets


@api.route("/full/")
class DatasetsFull(Resource):
    def get(self):
        """Return a list of all datasets known by the platform, along with their
        variables and time periods"""
        datasets = client.get_dataset_list()
        if len(datasets) == 0:
            abort(404)

        for dataset in datasets:
            dataset["info"] = client.get_parameters(dataset["ds_id"])
            if dataset["info"] is None:
                abort(404)

            datasets_fcts.process_parameters(
                dataset["info"],
                dataset_id=dataset["ds_id"],
                is_raster=dataset["is_raster"],
            )

        add_openaire_links(datasets)

        return datasets


@api.route("/<int:id>/parameters/")
class DatasetParameters(Resource):
    def get(self, id):
        """Return the variables and time periods available in a dataset"""
        parameters = client.get_parameters(id)
        if parameters is None:
            abort(404)

        datasets_fcts.process_parameters(parameters)

        return parameters


@api.route(
    "/layer_name/vector/<int:id>/", defaults={"variable": None, "time_period": None}
)
@api.route("/layer_name/vector/<int:id>/<string:variable>/<string:time_period>/")
@api.route(
    "/layer_name/vector/<int:id>/<string:variable>/", defaults={"time_period": None}
)
@api.route(
    "/layer_name/vector/<int:id>/-/<string:time_period>/",
    defaults={"variable": None},
)
class VectorLayerName(Resource):
    def get(self, id, variable=None, time_period=None):
        """Return an unique layer name"""
        if variable is not None:
            variable = variable.replace("__SLASH__", "/")

        layer_name = path.make_unique_layer_name(
            path.VECTOR, id, variable=variable, time_period=time_period
        )

        return Response(layer_name, mimetype="text/plain")


@api.route(
    "/layer_name/raster/<int:id>/", defaults={"variable": None, "time_period": None}
)
@api.route("/layer_name/raster/<int:id>/<string:variable>/<string:time_period>/")
@api.route(
    "/layer_name/raster/<int:id>/<string:variable>/", defaults={"time_period": None}
)
@api.route(
    "/layer_name/raster/<int:id>/-/<string:time_period>/",
    defaults={"variable": None},
)
class RasterLayerName(Resource):
    def get(self, id, variable=None, time_period=None):
        """Return an unique layer name"""
        if variable is not None:
            variable = variable.replace("__SLASH__", "/")

        layer_name = path.make_unique_layer_name(
            path.RASTER, id, variable=variable, time_period=time_period
        )

        return Response(layer_name, mimetype="text/plain")


@api.route("/legend/<path:layer_name>/")
class Legend(Resource):
    def get(self, layer_name):
        """Return the legend of the layer"""
        legend = client.get_legend(layer_name)
        if legend is None:
            abort(404)

        return legend


@api.route("/areas/")
class Areas(Resource):
    def get(self):
        """Return a list of all areas known by the platform"""
        areas = client.get_areas()
        if len(areas) == 0:
            abort(404)

        return areas


def add_openaire_links(datasets):
    for dataset in datasets:
        shared_id = dataset.get("shared_id")
        if not shared_id:
            dataset["openaireLink"] = "https://beta.openaire.eu/"
        else:
            shared_id_hash = hashlib.md5(shared_id.encode())  # nosec
            dataset[
                "openaireLink"
            ] = "https://beta.enermaps.openaire.eu/search/dataset?datasetId=enermaps____::{}".format(
                shared_id_hash.hexdigest()
            )
