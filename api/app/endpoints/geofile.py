"""Endpoint for the manipulation of geofiles
"""
import os

from flask import safe_join, send_file
from flask_restx import Namespace, Resource, abort
from werkzeug.datastructures import FileStorage

from app.common import projection
from app.models.geofile import Layer, get_user_upload

api = Namespace("geofile", description="Data management related endpoints")


upload_parser = api.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)


@api.route("/")
class GeoFiles(Resource):
    """Listing and creation of raster/shapefile"""

    def get(self):
        """Return a list of all geofile known by the system and accessible by the user making the request."""
        layers = Layer.list_layers()
        return {"files": [layer.name for layer in layers]}

    @api.expect(upload_parser)
    def post(self):
        """Add a geofile, currently only raster is supported in a geotiff format.

        Later we plan on supporting csv linking a NUTS (https://www.europeandataportal.eu/data/datasets?locale=en&tags=NUTS3&keywords=NUTS3&keywords=wfs&minScoring=0&page=1) to a value and shapefile.
        """
        args = upload_parser.parse_args()
        uploaded_file = args["file"]  # This is FileStorage instance
        layer = Layer.save(uploaded_file)
        if not layer.projection:
            layer.delete()
            abort(400, "The uploaded file didn't contain a projection")
        return {"status": "upload succeeded"}


@api.route("/<string:layer_name>")
class GeoFile(Resource):
    def get(self, layer_name):
        """Add a geofile, currently only raster is supported in a geotiff format."""
        Layer(layer_name)
        file_path = safe_join(get_user_upload(), layer_name)
        return send_file(file_path, attachment_filename=file_path)

    def delete(self, layer_name):
        """Remove a geofile by name."""
        Layer(layer_name).delete()
        return {"status": "deletion successfull"}
