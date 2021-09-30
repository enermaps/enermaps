"""Endpoint for the manipulation of datasets
"""

import hashlib

from flask_restx import Namespace, Resource, abort

from app.data_integration import enermaps_server as client

api = Namespace("datasets", description="Datasets related endpoints")


@api.route("/")
class Datasets(Resource):
    def get(self):
        """Return a list of all datasets known by the system"""
        datasets = client.get_dataset_list()

        # Construct the OpenAIRE link
        for dataset in datasets:
            shared_id = dataset.get("shared_id")
            if not shared_id:
                dataset["openairLink"] = "https://beta.openaire.eu/"
            else:
                shared_id_hash = hashlib.md5(shared_id.encode())  # nosec
                dataset[
                    "openairLink"
                ] = "https://beta.enermaps.openaire.eu/search/dataset?datasetId=enermaps____::{}".format(
                    shared_id_hash.hexdigest()
                )

        return datasets


@api.route("/<int:id>/variables/")
class DatasetVariables(Resource):
    def get(self, id):
        """Return the variables and time periods available in a dataset"""
        variables = client.get_variables(id)
        if variables is None:
            abort(404)

        # Ensure all fields have the format we want
        if ("variables" not in variables) or (variables["variables"] is None):
            variables["variables"] = []

        if ("time_periods" not in variables) or (variables["time_periods"] is None):
            variables["time_periods"] = []

        return variables
