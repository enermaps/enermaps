import os

from app.endpoints import cm, geofile, wms
from flask import Blueprint, Flask, redirect
from flask_restx import Api

from app.endpoints import cm, geofile, wms

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_DIR"] = "/tmp/upload_dir"
app.config["WMS"] = {}
app.config["WMS"]["ALLOWED_PROJECTIONS"] = ["ESPG:3857"]
app.config["WMS"]["MAX_SIZE"] = 1024 ** 2
app.config["WMS"]["GETMAP"] = {}
app.config["WMS"]["GETMAP"]["ALLOWED_OUTPUTS"] = ["image/png", "image/jpg"]
for k, v in app.config.items():
    app.config[k] = os.environ.get(k, v)
api_bp = Blueprint("api", "api", url_prefix="/api")
api = Api(api_bp)
api.add_namespace(geofile.api)
api.add_namespace(wms.api)
api.add_namespace(cm.api)
app.register_blueprint(api_bp)


@app.route("/")
def root_redirect():
    return redirect("/api")
