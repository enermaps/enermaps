"""Endpoint for the manipulation of datasets
"""

import base64
import hashlib

from flask import Response
from flask_restx import Namespace, Resource, abort

from app.common import client, path

api = Namespace("datasets", description="Datasets related endpoints")


@api.route("/")
class Datasets(Resource):
    def get(self):
        """Return a list of all datasets known by the platform"""
        datasets = client.get_dataset_list()

        add_openaire_links(datasets)

        return datasets


@api.route("/full/")
class DatasetsFull(Resource):
    def get(self):
        """Return a list of all datasets known by the platform, along with their
        variables and time periods"""
        datasets = client.get_dataset_list()

        for dataset in datasets:
            dataset["info"] = client.get_variables(dataset["ds_id"])
            if dataset["info"] is None:
                abort(404)

        add_openaire_links(datasets)

        return datasets


@api.route("/<int:id>/variables/")
class DatasetVariables(Resource):
    def get(self, id):
        """Return the variables and time periods available in a dataset"""
        variables = client.get_variables(id)
        if variables is None:
            abort(404)

        return variables


@api.route(
    "/layer_name/vector/<int:id>/", defaults={"variableb64": None, "time_period": None}
)
@api.route("/layer_name/vector/<int:id>/<string:variableb64>/<string:time_period>/")
@api.route(
    "/layer_name/vector/<int:id>/<string:variableb64>/", defaults={"time_period": None}
)
@api.route(
    "/layer_name/vector/<int:id>/-/<string:time_period>/",
    defaults={"variableb64": None},
)
class VectorLayerName(Resource):
    def get(self, id, variableb64=None, time_period=None):
        """Return an unique layer name"""
        if variableb64 is not None:
            variable = base64.b64decode(str.encode(variableb64)).decode()
        else:
            variable = None

        layer_name = path.make_unique_layer_name(
            path.VECTOR, id, variable=variable, time_period=time_period
        )

        return Response(layer_name, mimetype="text/plain")


@api.route(
    "/layer_name/raster/<int:id>/", defaults={"variableb64": None, "time_period": None}
)
@api.route("/layer_name/raster/<int:id>/<string:variableb64>/<string:time_period>/")
@api.route(
    "/layer_name/raster/<int:id>/<string:variableb64>/", defaults={"time_period": None}
)
@api.route(
    "/layer_name/raster/<int:id>/-/<string:time_period>/",
    defaults={"variableb64": None},
)
class RasterLayerName(Resource):
    def get(self, id, variableb64=None, time_period=None):
        """Return an unique layer name"""
        if variableb64 is not None:
            variable = base64.b64decode(str.encode(variableb64)).decode()
        else:
            variable = None

        layer_name = path.make_unique_layer_name(
            path.RASTER, id, variable=variable, time_period=time_period
        )

        return Response(layer_name, mimetype="text/plain")


@api.route("/legend/<path:layer_name>/")
class Legend(Resource):
    def get(self, layer_name):
        """Return a the legend of the layer"""
        return client.get_legend(layer_name)


@api.route("/areas/")
class Areas(Resource):
    def get(self):
        """Return a list of all areas known by the platform"""
        return client.get_areas()


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
