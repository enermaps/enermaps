#!/usr/bin/env python
from app.app import app

@api.route("/cm/<int:id_cm>/task/<int:task_id>")
class CM_fakeoutput(Resource):
    def get(self,id_cm,task_id):
        return send_file('./fakeoutput.json')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
