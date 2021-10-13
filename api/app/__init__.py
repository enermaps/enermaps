"""Entrypoint for the application.
This contains the initial creation of dataset in dev
mode and the initialisation of the applicaton.
"""
import logging
import os

from app.commands import cache
from app.endpoints import calculation_module, datasets, geofile, wms
from app.healthz import healthz
from app.redirect import redirect_to_api
from flask import Blueprint, Flask
from flask_restx import Api


class ReverseProxied(object):
    """WSGI middleware that ensure URLs are generated with the same protocol scheme
    that the request (HTTPS or HTTP)
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get("HTTP_X_FORWARDED_PROTO")
        if scheme:
            environ["wsgi.url_scheme"] = scheme

        return self.app(environ, start_response)


def create_app(environment="production", testing=False, on_startup=False):
    """Create the application and set the configuration.
    By default, testing mode is set to False."""

    # start by configuring the logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )

    # ok, we can now create our app
    app = Flask(__name__)
    app.config["TESTING"] = testing
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["MAX_PROJECTION_LENGTH"] = 1024
    app.config["RASTER_CACHE_DIR"] = None
    app.config["WMS_CACHE_DIR"] = "wms_cache"
    app.config["CM_OUTPUTS_DIR"] = "cm_outputs"
    app.config["FILTER_DATASETS"] = False
    app.config["WMS"] = {}
    app.config["WMS"]["ALLOWED_PROJECTIONS"] = ["EPSG:3857"]
    app.config["WMS"]["MAX_SIZE"] = 2048 ** 2
    app.config["WMS"]["GETMAP"] = {}
    app.config["WMS"]["GETMAP"]["ALLOWED_OUTPUTS"] = ["image/png", "image/jpg"]

    for k, v in app.config.items():
        app.config[k] = os.environ.get(k, v)

    api_bp = Blueprint("api", "api", url_prefix="/api")

    api = Api(api_bp)
    api.add_namespace(datasets.api)
    api.add_namespace(geofile.api)
    api.add_namespace(wms.api)
    api.add_namespace(calculation_module.api)

    app.register_blueprint(api_bp)
    app.register_blueprint(redirect_to_api)
    app.register_blueprint(healthz)

    app.cli.add_command(cache.update_all_datasets)
    app.cli.add_command(cache.update_dataset)
    app.cli.add_command(cache.update_areas)
    app.cli.add_command(cache.list_datasets)
    app.cli.add_command(cache.list_variables)

    # Install thr WSGI middleware
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    return app
