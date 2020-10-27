"""Description of each set of gis informations.

Modification of layer are made quite slow, so we don't
really prevent race condition on list vs delete. We 
also catch those on accessing the layer.

"""
import os

import mapnik
from flask import current_app, safe_join
from werkzeug.datastructures import FileStorage

from app.common.projection import proj4_from_geotiff


class Layer:
    def __init__(self, name):
        """Factory delegating to the child of the correct implementation
        according to a namespace in the name
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

    @staticmethod
    def save(file_upload: FileStorage):
        """Take an instance of a fileupload and create a layer from it.
        Return the resulting layer
        """
        return RasterLayer.save(file_upload)

    @staticmethod
    def load(name):
        return RasterLayer


def get_user_upload(user="user"):
    user_dir = safe_join(current_app.config["UPLOAD_DIR"], user)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir


class RasterLayer(Layer):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def list_layers():
        """As we store rasters on disk, we only want to list
        files in the directory.
        """
        user_dir = get_user_upload()
        layers = os.listdir(user_dir)
        return map(RasterLayer, layers)

    def _get_raster_path(self):
        layer_path = safe_join(get_user_upload(), self.name)
        return layer_path

    @property
    def projection(self):
        return proj4_from_geotiff(self._get_raster_path())

    def delete(self):
        """For raster, deleting a layer is equivalent to just removing
        the file.
        """
        os.unlink(self._get_raster_path())

    @staticmethod
    def save(file_upload: FileStorage):
        output_filepath = safe_join(get_user_upload(), file_upload.filename)
        file_upload.save(output_filepath)
        return RasterLayer(file_upload.filename)

    def get_mapnik_layer(self):
        # TODO: extract this from raster in advance
        layer = mapnik.Layer(self.name)
        layer_path = self._get_raster_path()
        layer.srs = self.projection
        # TODO: get this from the upload folder, check layer at that point ?
        gdal_source = mapnik.Gdal(file=layer_path)
        layer.datasource = gdal_source
        # layer.minimum_scale_denominator
        return layer


class VectorLayer(Layer):
    @staticmethod
    def list_layers():
        return []
