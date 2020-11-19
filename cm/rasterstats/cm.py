import os
from time import time

import numpy as np
from flask import send_file

import rasterio
from flask_restx import Namespace, Resource
from rasterstats import zonal_stats

api = Namespace("cm", "Calculation module endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))
file_test_dir = os.path.join(os.path.dirname(current_file_dir), "test_file")


@api.route("/<int:id_cm>/task/<int:task_id>")
class CM_fakeoutput(Resource):
    def get(self):
        fakeoutput = os.path.join(current_file_dir, "fakeoutput.json")
        return send_file(fakeoutput)
