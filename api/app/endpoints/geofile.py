"""Endpoint for the manipulation of geofiles
"""
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage

# from app.data_integration.data_config import get_legend, get_openair_link
from app.data_integration import data_endpoints
from app.models import geofile as geofile

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

        result = {layer.name: layer.as_dict() for layer in layers}
        for k, v in result.items():
            if k[0:2].isdigit():
                dataset_id = int(k[0:2])
                dataset_params = data_endpoints.get_ds(dataset_id)
                v["shared_id"] = dataset_params.get("shared_id", None)

        return result


@api.route("/<string:layer_name>/legend")
class GeofileLegend(Resource):
    def get(self, layer_name):
        """Get the layer legend: variable used for coloring the map, min and max values,
        list of rgb colors in order.
        """
        if layer_name[0:2].isdigit():
            layer_id = int(layer_name[0:2])
            return data_endpoints.get_legend(layer_id)
        return {}


@api.route("/<string:layer_name>/openair")
class GeofileOpenair(Resource):
    def get(self, layer_name):
        """Get the layer legend: variable used for coloring the map, min and max values,
        list of rgb colors in order.
        """
        if layer_name[0:2].isdigit():
            layer_id = int(layer_name[0:2])
            return data_endpoints.get_openair_link(layer_id)
        return {}


@api.route("/<string:layer_name>/type")
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
