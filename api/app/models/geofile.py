"""Description of each set of gis informations.

Modification of layer are made quite slow, so we don't
really prevent race condition on list vs delete. We
also catch those on accessing the layer.

"""
import io
import os
import shutil
import subprocess
import zipfile
from abc import ABC, abstractmethod
from glob import glob
from tempfile import TemporaryDirectory

import mapnik
from flask import current_app, safe_join
from werkzeug.datastructures import FileStorage

from app.common.projection import epsg_to_wkt, proj4_from_geotiff, proj4_from_shapefile


class SaveException(Exception):
    pass


def get_tmp_upload():
    """Return the buffer location for fetching file locally."""
    return get_user_upload("tmp")


def get_user_upload(subdirectory):
    """Return the location of a subdirectory for uploads. this also uses a
    subdirectories path component in the main user upload directory.
    This function is safe to path injection (such as .. in filename).
    This function will also care about directory creation if it doesn't exist
    yet"""
    user_dir = safe_join(current_app.config["UPLOAD_DIR"], subdirectory)
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
    if file_upload.mimetype in GeoJSONLayer.MIMETYPE:
        return GeoJSONLayer.save(file_upload)
    if file_upload.mimetype in VectorLayer.MIMETYPE:
        return VectorLayer.save(file_upload)
    elif file_upload.mimetype in RasterLayer.MIMETYPE:
        return RasterLayer.save(file_upload)
    raise Exception("Unknown file format {}".format(file_upload.mimetype))


def load(name):
    """Create a new instance of RasterLayer based on its name"""
    if name.endswith("zip") or name.endswith("geojson"):
        return VectorLayer(name)
    else:
        return RasterLayer(name)


class Layer(ABC):
    """This is a baseclass for the layers
    Each layer subclass have the set of method declared underneath.
    Each layer subclass also has a MIMETYPE constant which is a list
    of string mimetype. The first index of that array is the default
    mimetype of that layer used upon retrieving that layer.
    """

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
        layers = os.listdir(get_user_upload("raster"))
        non_hidden_layers = filter(lambda a: not a.startswith("."), layers)
        return map(RasterLayer, non_hidden_layers)

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
        with TemporaryDirectory(prefix=get_tmp_upload()) as tmp_dir:
            tmp_filepath = safe_join(tmp_dir, file_upload.filename)
            file_upload.save(tmp_filepath)
            output_filepath = safe_join(get_user_upload("raster"), file_upload.filename)
            os.replace(tmp_filepath, output_filepath)
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
        """Return a tuple (filedescriptor, mimetype) for the given layer
        raises:
            any error that can be raised by the open call.
        """
        file_descriptor = open(self._get_raster_path(), "rb")
        return file_descriptor, self.MIMETYPE[0]


class VectorLayer(Layer):
    """Future implementation of a vector layer."""

    MIMETYPE = ["application/zip"]

    def __init__(self, name):
        self.name = name

    def as_fd(self):
        """For shapefile, rezip the directory and send it.
        The created zipfile this will use in memory zip."""
        zipbuffer = io.BytesIO()
        vector_dir = self._get_vector_dir()
        with zipfile.ZipFile(zipbuffer, "a") as zip_file:
            for file_name in os.listdir(vector_dir):
                file_path = safe_join(vector_dir, file_name)
                with open(file_path, "rb") as fd:
                    zip_file.writestr(file_name, fd.read())
        zipbuffer.seek(0)
        return zipbuffer, self.MIMETYPE[0]

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
        """This is an atomic operation for saving the shapefile as a zip.
        We first unzipit to a tmp file in the same filesystem
        """
        try:
            zip_ref = zipfile.ZipFile(file_upload, "r")
        except zipfile.BadZipFile:
            raise SaveException("File is an invalid zip file.")
        # Use a temp file in the same directory as the ginal vector location
        # The point here is to have an atomic replace which is only possible if
        # the origin and the destination are in the same filesystem.
        with TemporaryDirectory(prefix=get_tmp_upload()) as tmp_dir:
            zip_ref.extractall(tmp_dir)
            upload_dir = get_user_upload("vectors")
            output_dirpath = safe_join(upload_dir, file_upload.filename)
            os.replace(tmp_dir, output_dirpath)
        return VectorLayer(file_upload.filename)

    @staticmethod
    def list_layers():
        """List file in the vector directory
        Ignore hidden file as they are used for unzipping destination and don't
        provide ondisk consistency.
        """
        layers = os.listdir(get_user_upload("vectors"))
        non_hidden_layers = filter(lambda a: not a.startswith("."), layers)
        return map(VectorLayer, non_hidden_layers)

    def delete(self):
        shutil.rmtree(self._get_vector_dir())


class GeoJSONLayer(VectorLayer):
    """This is just a shim to the VectorLayer, we take a geojson as input in the
    save method, then transform it to a shapefile directory containing a proj file
    and a shp file.
    """

    MIMETYPE = ["application/json", "application/geojson", "application/geo+json"]
    DEFAULT_PROJECTION = epsg_to_wkt(4326)

    def save(file_upload: FileStorage):
        """This method takes a geojson as input and present it as a raster file"""
        with TemporaryDirectory(prefix=get_tmp_upload()) as tmp_dir:
            tmp_filepath = safe_join(tmp_dir, file_upload.filename)
            file_upload.save(tmp_filepath)
            shape_name, _ = os.path.splitext(file_upload.filename)
            shapefile_filepath = safe_join(tmp_dir, shape_name + ".shp")
            args = ["ogr2ogr", "-f", "ESRI Shapefile", shapefile_filepath, tmp_filepath]
            try:
                subprocess.check_call(args)
            except subprocess.CalledProcessError:
                raise SaveException("File cannot be encoded into a shapefile")
            proj_filepath = safe_join(tmp_dir, shape_name + ".prj")
            # geojson can use a single projection,
            # so create that file with the standard geojson projection
            with open(proj_filepath, "w") as fd:
                fd.write(GeoJSONLayer.DEFAULT_PROJECTION)
            os.remove(tmp_filepath)

            # everything went fine, symlink and return the corresponding VectorLayer
            upload_dir = get_user_upload("vectors")
            output_dirpath = safe_join(upload_dir, shape_name + ".geojson")
            os.replace(tmp_dir, output_dirpath)
        return VectorLayer(shape_name + ".geojson")
