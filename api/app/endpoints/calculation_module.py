import os

from flask import request
from flask_restx import Namespace, Resource

from app.models import calculation_module as CM

api = Namespace("cm", "Calculation module endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))


@api.route("/")
class CMList(Resource):
    def get(self):
        cms = CM.list_cms()

        def cm_as_dict(cm):
            ret = {}
            ret["parameters"] = cm.params
            ret["name"] = cm.name
            ret["schema"] = cm.schema
            return ret

        return {"cms": [cm_as_dict(cm) for cm in cms.values()]}


@api.route("/<string:cm_name>/task")
class TaskCreator(Resource):
    def post(self, cm_name):
        cm = CM.cm_by_name(cm_name)
        create_task_parameters = request.get_json()
        selection = create_task_parameters["selection"]
        layers = create_task_parameters["layers"]
        parameters = create_task_parameters["parameters"]
        task = cm.call(selection, layers, parameters)
        return {"task_id": task.id}


@api.route("/<string:cm_name>/task/<string:task_id>")
class CM_fakeoutput(Resource):
    def delete(self, cm_name, task_id):
        res = CM.task_by_id(task_id, cm_name=cm_name)
        res.revoke()
        return {"status": res.status}

    def get(self, cm_name, task_id):
        task = CM.task_by_id(task_id, cm_name=cm_name)
        if not task.ready():
            return {"status": task.status}
        try:
            result = task.get(timeout=0.5)
        except Exception as e:
            if task.status == 'FAILURE':
                # this is an expected failure
                return {"status": task.status, "exception": str(e)}
        return {"status": task.status, "result": result}
