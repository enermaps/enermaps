"""Entrypoint for the application.
This contains the initial creation of dataset in dev
mode and the initialisation of the applicaton.
"""
import io
import os

import requests
from flask import Blueprint, Flask
from flask_restx import Api
from werkzeug.datastructures import FileStorage

from app.endpoints import calculation_module, geofile, wms
from app.healthz import healthz
from app.models.geofile import create, list_layers
from app.redirect import redirect_to_api


def fetch_dataset(base_url, get_parameters, filename, content_type):
    """Get a single zip dataset and import it into enermaps."""
    existing_layers_name = [layer.name for layer in list_layers()]
    if filename in existing_layers_name:
        print("Not fetching {}, we already have it locally".format(filename))
        return
    print("Fetching " + filename)
    with requests.get(base_url, params=get_parameters, stream=True) as resp:
        resp_data = io.BytesIO(resp.content)
    file_upload = FileStorage(resp_data, filename, content_type=content_type)
    create(file_upload)


def init_datasets():
    """If the dataset was found to be empty, initialize the datasets for
    the selection of:
    * NUTS(0|1|2|3)
    * LAU
    * And an overlay layer!

    Currently, we fetch the dataset from hotmaps.eu
    """
    print("Ensure we have the initial set of dataset")
    base_url = "https://geoserver.hotmaps.eu/geoserver/hotmaps/ows"
    base_query_params = {
        "service": "WFS",
        "version": "1.0.0",
        "request": "GetFeature",
        "outputFormat": "SHAPE-ZIP",
    }
    nuts_query = {**base_query_params, **{"typeName": "hotmaps:nuts"}}
    cql_filter = "stat_levl_='{!s}' AND year='2013-01-01'"
    lau_query = {**base_query_params, **{"typeName": "hotmaps:tbl_lau1_2"}}
    for i in range(4):
        nuts_query["CQL_FILTER"] = cql_filter.format(i)
        filename = "nuts{!s}.zip".format(i)
        fetch_dataset(base_url, nuts_query, filename, "application/zip")

    # TODO replace with data from the database
    filename = "lau.zip"
    fetch_dataset(base_url, lau_query, filename, "application/zip")

    tif_query = {
        "service": "WMS",
        "version": "1.1.0",
        "request": "GetMap",
        "layers": "hotmaps:gfa_tot_curr_density",
        "styles": "",
        "bbox": "944000.0,938000.0,6528000.0,5414000.0",
        "width": 768,
        "height": 615,
        "srs": "EPSG:3035",
        "format": "image/geotiff",
    }
    filename = "gfa_tot_curr_density.tiff"
    fetch_dataset(base_url, tif_query, filename, "image/tiff")


def create_app(environment="production", testing=False):
    """Create the application and set the configuration.
    By default, testing mode is set to False."""
    app = Flask(__name__)
    app.config["TESTING"] = testing
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["MAX_PROJECTION_LENGTH"] = 1024
    app.config["UPLOAD_DIR"] = "/tmp/upload_dir"
    app.config["WMS"] = {}
    app.config["WMS"]["ALLOWED_PROJECTIONS"] = ["EPSG:3857"]
    app.config["WMS"]["MAX_SIZE"] = 2048 ** 2
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
    app.register_blueprint(healthz)
    with app.app_context():
        if not app.testing:
            init_datasets()
    return app
