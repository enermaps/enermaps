"""Set of endpoints for the management of calculation module.

Calculation modules are long running tasks ran on a raster
with a selection.
"""
import os

from flask import abort, redirect, request, url_for
from flask_restx import Namespace, Resource

from app.models import calculation_module as CM

api = Namespace("cm", "Calculation module endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))


@api.route("/")
class CMList(Resource):
    def get(self):
        """List all cms available on a celery queue,
        and return them in dictionary.
        """
        cms = CM.list_cms()

        def cm_as_dict(cm):
            ret = {}
            ret["parameters"] = cm.params
            ret["name"] = cm.name
            ret["pretty_name"] = cm.pretty_name
            ret["schema"] = cm.schema
            return ret

        return {"cms": [cm_as_dict(cm) for cm in cms.values()]}


@api.route("/<string:cm_name>/task")
class TaskCreator(Resource):
    def post(self, cm_name):
        """Create a new task from CM name, generate a task ID,
        and redirect the user to
        "cm/<string:cm_name>/task/<string:task_id>".
        """
        try:
            cm = CM.cm_by_name(cm_name)
        except CM.UnexistantCalculationModule as err:
            abort(404, description=str(err))
        create_task_parameters = request.get_json()
        selection = create_task_parameters.get("selection", {})
        layers = create_task_parameters.get("layers", [])
        parameters = create_task_parameters.get("parameters", {})
        task = cm.call(selection, layers, parameters)
        return redirect(url_for(".cm_cm_task", cm_name=cm_name, task_id=task))


@api.route("/<string:cm_name>/task/<string:task_id>")
class CMTask(Resource):
    def delete(self, cm_name, task_id):
        """Delete task based on the CM name and the task ID,
        and redirect the user to
        "cm/<string:cm_name>/task/<string:task_id>".
        """
        res = CM.task_by_id(task_id, cm_name=cm_name)
        res.revoke(terminate=True)
        return redirect(url_for(".cm_cm_task", cm_name=cm_name, task_id=task_id))

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
                task_status["result"] = "An unexpected error happened"
        else:
            task_status["result"] = result
        return task_status