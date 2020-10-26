from flask import send_file
from flask_restx import Namespace, Resource
import os

api = Namespace("cm", "Calculation module endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))


@api.route("/<int:id_cm>/task/<int:task_id>")
class CM_fakeoutput(Resource):
    def get(self, id_cm, task_id):
        fakeoutput = os.path.join(current_file_dir, "fakeoutput.json")
        return send_file(fakeoutput)
