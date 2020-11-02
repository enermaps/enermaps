"""Description of each set of gis informations.

Modification of layer are made quite slow, so we don't
really prevent race condition on list vs delete. We
also catch those on accessing the layer.

"""
import os
from glob import glob
import shutil
import zipfile
from abc import ABC, abstractmethod

import mapnik
from flask import current_app, safe_join
from werkzeug.datastructures import FileStorage

from app.common.projection import proj4_from_geotiff, proj4_from_shapefile


def get_user_upload(prefix_path):
    """Return the location of a subdirectory for uploads. this also uses a prefix"""
    user_dir = safe_join(current_app.config["UPLOAD_DIR"], prefix_path)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir


def list_layers():
    """Return the list of all layers from all direct subclasses
    of Layer
    """
    layers = []
    for layer_type in Layer.__subclasses__():
        layers += layer_type.list_layers()
    return layers


def create(file_upload: FileStorage):
    """Take an instance of a fileupload and create a layer from it.
    Return the resulting layer
    """
    if file_upload.mimetype in VectorLayer.MIMETYPE:
        return VectorLayer.save(file_upload)
    elif file_upload.mimetype in RasterLayer.MIMETYPE:
        return RasterLayer.save(file_upload)
    raise Exception("Unknown file format {}".format(file_upload.mimetype))


def load(name):
    """Create a new instance of RasterLayer based on its name"""
    if name.endswith("zip"):
        return VectorLayer(name)
    else:
        return RasterLayer(name)


class Layer(ABC):
    @abstractmethod
    def as_fd(self):
        pass

    @abstractmethod
    def as_mapnik_layer(self):
        pass

    @property
    @abstractmethod
    def projection(self):
        pass

    @property
    @abstractmethod
    def is_queryable(self):
        """Return true if the layer has features, this allow the layer to be
        queried for feature at a given location
        """
        pass

    @staticmethod
    @abstractmethod
    def save(file_upload: FileStorage):
        pass

    @staticmethod
    @abstractmethod
    def list_layers(file_upload: FileStorage):
        pass

    @abstractmethod
    def delete(self):
        pass


class RasterLayer(Layer):

    # mimetype for a rasterlayer, the first mimetype is the one
    # chosen by default for exposing the file
    MIMETYPE = ["image/geotiff", "image/tiff"]

    def __init__(self, name):
        self.name = name

    @staticmethod
    def list_layers():
        """As we store rasters on disk, we only want to list
        files in the directory.
        """
        user_dir = get_user_upload("raster")
        layers = os.listdir(user_dir)
        return map(RasterLayer, layers)

    def _get_raster_path(self):
        """Return the path where a raster is stored on disk."""
        layer_path = safe_join(get_user_upload("raster"), self.name)
        return layer_path

    @property
    def is_queryable(self):
        return False

    @property
    def projection(self):
        """Return the projection of the raster layer,
        currently this approach is quite naive as we read
        from the disk to only extract the projection.
        """
        return proj4_from_geotiff(self._get_raster_path())

    def delete(self):
        """Delete a raster file.

        For raster, deleting a layer is equivalent to just removing
        the file.
        """
        os.unlink(self._get_raster_path())

    @staticmethod
    def save(file_upload: FileStorage):
        output_filepath = safe_join(get_user_upload("raster"), file_upload.filename)
        file_upload.save(output_filepath)
        return RasterLayer(file_upload.filename)

    def as_mapnik_layer(self):
        # TODO: extract this from raster in advance
        layer = mapnik.Layer(self.name)
        layer_path = self._get_raster_path()
        layer.srs = self.projection
        # TODO: get this from the upload folder, check layer at that point ?
        gdal_source = mapnik.Gdal(file=layer_path)
        layer.datasource = gdal_source
        layer.queryable = False
        # layer.minimum_scale_denominator
        return layer

    def as_fd(self):
        """Return a tuple filedescriptor/mimetype for the given layer"""
        return open(self._get_raster_path(), "rb"), self.MIMETYPE[0]


class VectorLayer(Layer):
    """Future implementation of a vector layer."""

    MIMETYPE = "application/zip"

    def __init__(self, name):
        self.name = name

    def as_fd(self):
        """For shapefile, rezip the directory and send it"""

    def as_mapnik_layer(self):
        layer = mapnik.Layer(self.name)
        shapefiles = glob(os.path.join(self._get_vector_dir(), "*.shp"))
        if not shapefiles:
            raise FileNotFoundError("Shapefile was not found")
        layer.srs = self.projection
        layer.datasource = mapnik.Shapefile(file=shapefiles[0])
        layer.queryable = True
        return layer

    def _get_vector_dir(self):
        return safe_join(get_user_upload("vectors"), self.name)

    @property
    def projection(self):
        vector_dir = self._get_vector_dir()
        return proj4_from_shapefile(vector_dir)

    @property
    def is_queryable(self):
        """Return true if the layer has features, this allow the layer to be
        queried for feature at a given location
        """
        return True

    @staticmethod
    def save(file_upload: FileStorage):
        tmp_path = "/tmp/test.zip"
        file_upload.save(tmp_path)
        zip_ref = zipfile.ZipFile(tmp_path, "r")
        output_dirpath = safe_join(get_user_upload("vectors"), file_upload.filename)
        zip_ref.extractall(output_dirpath)
        return VectorLayer(file_upload.filename)

    @staticmethod
    def list_layers():
        layers = os.listdir(get_user_upload("vectors"))
        return map(VectorLayer, layers)

    def delete(self):
        shutil.rmtree(self._get_vector_dir())
