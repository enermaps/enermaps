"""Set of endpoints for the management of calculation module.

Calculation modules are long running tasks ran on a raster
with a selection.
"""
import os
import re
import unicodedata

from flask import Response, abort, redirect, request, url_for
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage

from app.common import path
from app.models import calculation_module as CM
from app.models import geofile, storage

api = Namespace("cm", "Calculation module endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))


upload_parser = api.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)


@api.route("/")
class CMList(Resource):
    def get(self):
        """List all cms available on a celery queue,
        and return them in dictionary.
        """
        cms = CM.list_cms()

        def cm_as_dict(cm):
            ret = {}
            ret["name"] = cm.name
            ret["pretty_name"] = cm.pretty_name
            ret["parameters"] = cm.parameters
            ret["schema"] = cm.schema
            return ret

        return [cm_as_dict(cm) for cm in cms.values()]


@api.route("/<string:cm_name>/task/")
class CMTaskCreator(Resource):
    def post(self, cm_name):
        """Create a new task from CM name, generate a task ID,
        and redirect the user to
        "cm/<string:cm_name>/task/<string:task_id>".
        """
        try:
            cm = CM.cm_by_name(cm_name)
        except CM.UnexistantCalculationModule as err:
            abort(404, description=str(err))

        input_parameters = request.get_json()

        selection = input_parameters.get("selection", {})
        layer_name = input_parameters.get("layer", None)
        parameters = input_parameters.get("parameters", {})

        # Retrieve the list of TIFF files associated with the layer
        layers = []
        if (layer_name is not None) and (path.get_type(layer_name) == path.RASTER):
            storage_instance = storage.create(layer_name)
            root_dir = storage_instance.get_root_dir()
            for feature_id in storage_instance.list_feature_ids(layer_name):
                file_path = storage_instance.get_file_path(layer_name, feature_id)
                layers.append(file_path.replace(root_dir + os.path.sep, ""))

        task = cm.call(selection, layers, parameters)

        layer_name = path.make_unique_layer_name(path.CM, cm_name, task_id=task)
        geofile.save_cm_parameters(layer_name, input_parameters)

        return redirect(url_for(".cm_cm_task", cm_name=cm_name, task_id=task))


@api.route("/<string:cm_name>/task/<string:task_id>/")
class CMTask(Resource):
    def delete(self, cm_name, task_id):
        """Delete task based on the CM name and the task ID,
        and redirect the user to
        "cm/<string:cm_name>/task/<string:task_id>".
        """
        res = CM.task_by_id(task_id, cm_name=cm_name)
        res.revoke(terminate=True)
        return {"status": "REVOKED", "task_id": task_id, "cm_name": cm_name}

    def get(self, cm_name, task_id):
        """Get task based on the CM name and the task ID,
        and return a dictionary as response.
        If task hasn't executed yet, empty dictionary is returned.
        """
        task = CM.task_by_id(task_id, cm_name=cm_name)

        task_status = {"status": task.status, "task_id": task_id, "cm_name": cm_name}
        if not task.ready():
            task_status["result"] = ""
            return task_status

        try:
            result = task.get(timeout=0.5)
        except Exception as e:
            if task.status == "FAILURE":
                # this is an expected failure
                task_status["result"] = str(e)
            else:
                task_status["status"] = "FAILURE"
                task_status["result"] = "An unexpected error happened: " + str(e)
        else:
            task_status["result"] = result
            layer_name = path.make_unique_layer_name(path.CM, cm_name, task_id=task_id)
            geofile.save_cm_result(layer_name, result)

        return task_status


@api.route("/<string:cm_name>/task/<string:task_id>/geofile/")
class CMTaskGeofile(Resource):
    @api.expect(upload_parser)
    def post(self, cm_name, task_id):
        args = upload_parser.parse_args()
        uploaded_file = args["file"]  # This is FileStorage instance

        layer_name = path.make_unique_layer_name(path.CM, cm_name, task_id=task_id)

        # Generate a safe filename from the actuel name of the file
        feature_id = (
            uploaded_file.filename.strip().replace(".tiff", ".tif").replace(" ", "_")
        )
        feature_id = (
            unicodedata.normalize("NFKD", feature_id)
            .encode("ASCII", "ignore")
            .decode("utf-8")
        )
        feature_id = re.sub(r"(?u)[^-\w.]", "", feature_id)
        feature_id = re.sub(r"^(\.+)", "", feature_id)

        # Save the file
        if not geofile.save_cm_file(layer_name, feature_id, uploaded_file.read()):
            abort(400)

        return Response(status=201)
