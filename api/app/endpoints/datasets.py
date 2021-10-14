"""Endpoint for the manipulation of datasets
"""

import base64
import hashlib

from flask import Response
from flask_restx import Namespace, Resource, abort

from app.common import path
from app.data_integration import data_endpoints
from app.data_integration import enermaps_server as client

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
    "/<int:id>/layer_name/vector/", defaults={"variableb64": None, "time_period": None}
)
@api.route("/<int:id>/layer_name/vector/<string:variableb64>/<string:time_period>/")
@api.route(
    "/<int:id>/layer_name/vector/<string:variableb64>/", defaults={"time_period": None}
)
@api.route(
    "/<int:id>/layer_name/vector/-/<string:time_period>/",
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
    "/<int:id>/layer_name/raster/", defaults={"variableb64": None, "time_period": None}
)
@api.route("/<int:id>/layer_name/raster/<string:variableb64>/<string:time_period>/")
@api.route(
    "/<int:id>/layer_name/raster/<string:variableb64>/", defaults={"time_period": None}
)
@api.route(
    "/<int:id>/layer_name/raster/-/<string:time_period>/",
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
        (_, layer_id, _, _, _) = path.parse_unique_layer_name(layer_name)
        return data_endpoints.get_legend(layer_id)


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
