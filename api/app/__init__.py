import os
import io

from flask import Blueprint, Flask
from flask_restx import Api
import requests
from werkzeug.datastructures import FileStorage

from app.endpoints import calculation_module, geofile, wms
from app.redirect import redirect_to_api
from app.models.geofile import create, list_layers


def init_dataset():
    """If the dataset was found to be empty, initialize the datasets for
    the selection of:
    * NUTS(0|1|2|3)
    * LAU

    Currently, we fetch the dataset from hotmaps.eu
    """
    print("Ensure we have the initial dataset")
    existing_layers_name = [layer.name for layer in list_layers()]
    nuts_base_url = "https://geoserver.hotmaps.eu/geoserver/hotmaps/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hotmaps:nuts&outputFormat=SHAPE-ZIP&CQL_FILTER=stat_levl_=%27{!s}%27%20AND%20year=%272013-01-01%27"
    lau_url = "https://geoserver.hotmaps.eu/geoserver/hotmaps/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hotmaps:tbl_lau1_2&outputFormat=SHAPE-ZIP"
    for i in range(4):
        filename = "nuts{!s}.zip".format(i)
        if filename in existing_layers_name:
            print("Not fetching {}, we already have it locally".format(filename))
            continue
        print("Fetching " + filename)
        url = nuts_base_url.format(i)
        resp = requests.get(url, stream=True)
        file_upload = FileStorage(resp.raw, filename)
        create(file_upload)

    filename = "lau.zip"
    if filename in existing_layers_name:
        print("Not fetching {}, we already have it locally".format(filename))
        return
    print("Fetching lau")
    resp = requests.get(lau_url, stream=True)
    file_upload = FileStorage(resp.raw, "lau.zip")
    create(file_upload)
    return


def create_app(environment="production", testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = testing
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["MAX_PROJECTION_LENGTH"] = 1024
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
    api.add_namespace(calculation_module.api)
    app.register_blueprint(api_bp)
    app.register_blueprint(redirect_to_api)
    with app.app_context():
        if not app.testing:
            init_dataset()
    return app
