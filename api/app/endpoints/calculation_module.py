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
            ret["params"] = cm.params
            ret["name"] = cm.name
            ret["schema"] = cm.schema
            return ret

        return {"cms": [cm_as_dict(cm) for cm in cms.values()]}


@api.route("/<string:cm_name>/task")
class TaskCreator(Resource):
    def post(self, cm_name):
        cm = CM.cm_by_name(cm_name)
        task = cm.call(**request.params)
        return {"task_id": task.id}


@api.route("/<string:cm_name>/task/<string:task_id>")
class CM_fakeoutput(Resource):
    def delete(self, cm_name, task_id):
        res = CM.task_by_id(task_id, cm_name=cm_name)
        res.revoke()
        return {"status": res.status}

    def get(self, cm_name, task_id):
        res = CM.task_by_id(task_id, cm_name=cm_name)
        print(res.result)
        if res.failed():
            return {"status": res.status, "error": res.result}
        if res.successful():
            return {"status": res.status, "result": res.result}
        return {"status": res.status}
