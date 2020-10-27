"""Description of each set of gis informations.
"""
import os
import mapnik

from flask import current_app, safe_join

from app.common.projection import proj4_from_geotiff

class Layer():
    def __init__(self, name):
        """Factory delegating to the child of the correct implementation according to a namespace in the name
        """
        self.name = name

    @staticmethod
    def list_layers():
        """Return the list of all layers from all direct subclasses 
        of Layer
        """
        layers = []
        for layer_type in Layer.__subclasses__():
            layers += layer_type.list_layers()
        return layers


def get_user_upload(user="user"):
    user_dir = safe_join(current_app.config["UPLOAD_DIR"], user)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir


class RasterLayer(Layer):
    def __init__(self, name):
        self.name = name
        layer_path = self._get_raster_path()
        if not os.path.isfile(layer_path):
            raise FileNotFoundError("layer not found")

    @staticmethod
    def list_layers():
        user_dir = get_user_upload()
        layers = os.listdir(user_dir)
        return map(RasterLayer, layers)

    @staticmethod
    def create_from_bytes():
        pass

    def _get_raster_path(self):
        layer_path = safe_join(get_user_upload(), self.name)
        return layer_path

    @property
    def projection(self):
        proj4_from_geotiff(self._get_raster_path())


    def get_mapnik_layer(self):
        # TODO: extract this from raster in advance
        RasterLayer(self.name)
        layer_path = self._get_raster_path()
        layer.srs = self.projection
        print(layer.srs)
        # TODO: get this from the upload folder, check layer at that point ?
        gdal_source = mapnik.Gdal(file=layer_path)
        layer.datasource = gdal_source
        # layer.minimum_scale_denominator
        return layer



class VectorLayer(Layer):
    @staticmethod
    def list_layers():
        return []

    @staticmethod
    def create_from_bytes():
        pass
