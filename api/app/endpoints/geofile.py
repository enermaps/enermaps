"""Endpoint for the manipulation of geofiles
"""
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage

from app.data_integration import data_endpoints

api = Namespace("geofile", description="Data management related endpoints")


upload_parser = api.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)


@api.route("/<string:layer_name>/legend/")
class GeofileLegend(Resource):
    def get(self, layer_name):
        """Get the layer legend: variable used for coloring the map, min and max values,
        list of rgb colors in order.
        """
        if layer_name[0:2].isdigit():
            layer_id = int(layer_name[0:2])
            return data_endpoints.get_legend(layer_id)
        return {}


@api.route("/<string:layer_name>/openair/")
class GeofileOpenair(Resource):
    def get(self, layer_name):
        """Get the layer legend: variable used for coloring the map, min and max values,
        list of rgb colors in order.
        """
        if layer_name[0:2].isdigit():
            layer_id = int(layer_name[0:2])
            return data_endpoints.get_openair_link(layer_id)
        return {}


@api.route("/<string:layer_name>/type/")
class GeofileType(Resource):
    def get(self, layer_name):
        """Get the layer legend: variable used for coloring the map, min and max values,
        list of rgb colors in order.
        """
        if layer_name[0:2].isdigit():
            layer_id = int(layer_name[0:2])
            layer_type, data_type = data_endpoints.get_ds_type(layer_id)
            return {"layer_type": layer_type, "data_type": data_type}
        return {"layer_type": "", "data_type": ""}
