"""Endpoint for the manipulation of geofiles
"""
from flask import redirect, send_file, url_for
from flask_restx import Namespace, Resource, abort
from werkzeug.datastructures import FileStorage

import app.models.geofile as geofile

api = Namespace("geofile", description="Data management related endpoints")


upload_parser = api.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)


@api.route("/")
class GeoFiles(Resource):
    """Listing and creation of raster/shapefile"""

    def get(self):
        """Return a list of all geofile known by
        the system and accessible by the user making the request."""
        layers = geofile.list_layers()
        return {layer.name: layer.as_dict() for layer in layers}

    @api.expect(upload_parser)
    def post(self):
        """Add a geofile, currently only raster is supported in a geotiff format.

        Later we plan on supporting
        * csv: linking a NUTS to a value and shapefile.
        """
        args = upload_parser.parse_args()
        uploaded_file = args["file"]  # This is FileStorage instance
        # TODO this should be in the error handler instead
        try:
            layer = geofile.create(uploaded_file)
        except geofile.SaveException as e:
            abort(400, str(e))
        if not layer.projection:
            layer.delete()
            abort(400, "The uploaded file didn't contain a projection")
        return redirect(url_for(".geofile_geo_files"))


@api.route("/<string:layer_name>")
class GeoFile(Resource):
    def get(self, layer_name):
        """Get a geofile, currently shapefile as zip
        and raster as geotiff is supported."""
        layer = geofile.load(layer_name)
        layer_fd, mimetype = layer.as_fd()
        return send_file(layer_fd, mimetype=mimetype)

    def delete(self, layer_name):
        """Remove a geofile by name."""
        geofile.load(layer_name).delete()
        return redirect(url_for(".geofile_geo_files"))
