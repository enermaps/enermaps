import os

from celery import Celery, result
from flask import send_file
from flask_restx import Namespace, Resource

from app.models import CMTask

api = Namespace("cm", "Calculation module endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))
app = Celery(broker="redis://guest@localhost//", backend="redis://localhost")
app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="Europe/Zurich",
    enable_utc=True,
)

cms = CMTask.list_tasks(app)
@api.route("/")
class CMList(Resource):
    def get(self):
        global cms
        cms = CMTask.list_tasks(app)
        return {"cms": list(cms.keys())}


@api.route("/<string:cm_name>/task")
class TaskCreator(Resource):
    def post(self, cm_name):
        task = cms[cm_name].call('')
        return {'task_id': task.id}


@api.route("/<string:cm_name>/task/<string:task_id>")
class CM_fakeoutput(Resource):
    def delete(self, cm_name, task_id):
        res = app.AsyncResult(task_id, task_name=cm_name)
        res.revoke()
        return {'status': res.status}

    def get(self, cm_name, task_id):
        res = app.AsyncResult(task_id, task_name=cm_name)
        print(res.result)
        if res.failed():
            return {"status": res.status, "error": res.result}
        if res.successful():
            return {"status": res.status, "result": res.result}
        return {"status": res.status}
