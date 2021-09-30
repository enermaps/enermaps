"""Description of each set of gis informations.

Modification of layer are made quite slow, so we don't
really prevent race condition on list vs delete. We
also catch those on accessing the layer.

"""
import io
import os
import shutil
import subprocess  # nosec
import zipfile
from abc import ABC, abstractmethod
from glob import glob
from pathlib import Path
from tempfile import TemporaryDirectory

import mapnik
from flask import current_app, safe_join
from PIL import Image
from werkzeug.datastructures import FileStorage

from app.common.projection import proj4_from_geotiff  # epsg_to_proj4,
from app.common.projection import epsg_to_wkt, proj4_from_shapefile


class SaveException(Exception):
    """Exception thrown when saving geofile is not possible."""

    pass


def get_tmp_geodb_dir():
    """Return the buffer location for fetching file locally."""
    return get_geodb_subfolder("tmp")


def get_tmp_cm_outputs_dir():
    """Return the buffer location for fetching file locally."""
    tmp_dir = safe_join(current_app.config["CM_OUTPUTS_DIR"], "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


def get_geodb_subfolder(subdirectory):
    """Return the location of a subdirectory for geodbs. This also uses a
    subdirectories path component in the main geodb directory.
    This function is safe to path injection (such as .. in filename).
    This function will also care about directory creation if it doesn't exist
    yet.
    Path example : /geodb/subdirectory
    """
    subdir = safe_join(current_app.config["GEODB_CACHE_DIR"], subdirectory)
    os.makedirs(subdir, exist_ok=True)
    return subdir


def list_layers():
    """Return the list of all layers from all direct subclasses
    of Layer class.
    """

    def list_subclass_layers(cl):
        layers = []
        for subclass in cl.__subclasses__():
            if subclass not in [CMRasterLayer]:
                layers += subclass.list_layers()
                layers += list_subclass_layers(subclass)
        return layers

    return list_subclass_layers(Layer)


def list_cm_outputs():
    """Return the list of all cm_outputs"""
    return CMRasterLayer.list_layers()


def create(file_upload: FileStorage, is_cm_output=False):
    """Take an instance of a fileupload and create a layer from it.
    Return the resulting layer
    """
    if file_upload.mimetype in GeoJSONLayer.MIMETYPE:
        return GeoJSONLayer.save(file_upload)
    if file_upload.mimetype in VectorLayer.MIMETYPE:
        return VectorLayer.save(file_upload)
    if file_upload.mimetype in RasterLayer.MIMETYPE:
        if is_cm_output:
            return CMRasterLayer.save(file_upload)
        else:
            return RasterLayer.save(file_upload)
    raise Exception("Unknown file format {}".format(file_upload.mimetype))


def load(name):
    """Create a new instance of RasterLayer based on its name"""
    if name.startswith("cm_outputs/"):
        _, name = name.split("/")
        return load_cm_output(name)

    if name.endswith("zip") or name.endswith("geojson"):
        return VectorLayer(name)
    elif name.endswith("tif") or name.endswith("tiff"):
        return RasterLayer(name)


def load_cm_output(name):
    """Create a new instance of RasterLayer based on its name"""
    layer = CMRasterLayer(name)
    if layer.exists():
        layer.touch()
        return layer

    raise FileNotFoundError


class Layer(ABC):
    """This is a baseclass for the layers
    Each layer subclass have the set of method declared underneath.
    Each layer subclass also has a MIMETYPE constant which is a list
    of string mimetype. The first index of that array is the default
    mimetype of that layer used upon retrieving that layer.
    """

    def __init__(self, name):
        # The layer name is the full name "layerId_layerName_extension"
        self.name = name

    @abstractmethod
    def as_fd(self):
        """Return the Layer as an open file descriptor.

        A warning here, the closing of the file descriptor is left for the
        callee.
        """
        pass

    @abstractmethod
    def as_mapnik_layer(self):
        """Return the Layer as a mapnik layer
        (https://mapnik.org/docs/v2.2.0/api/python/mapnik._mapnik.Layer-class.html)
        """
        pass

    @property
    @abstractmethod
    def projection(self):
        """Return the projection used for that datasource, the output is always a proj4 string
        (see https://proj.org/ for more information)
        """
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
        """Save the FileStorage instance as a geofile.
        This method will return an instance of the class.
        The operation must guarantee atomicity, meaning the save operation can be
        interupted at any moment and it shouldn't left half deleted file around.
        """
        pass

    @staticmethod
    @abstractmethod
    def list_layers():
        """List all layers abstracted by the current class.
        This method returns a list of instance of the class.
        """
        pass

    @abstractmethod
    def delete(self):
        """Remove the geofile from the geofile database.
        This operation must also guarantee to be atomic, so you can end up
        with a half deleted datasource.
        """
        pass

    def as_dict(self):
        """Return a description of this layer as a dict. This is a very short version of metadata"""
        return {
            "isQueryable": self.is_queryable,
        }

    @property
    def metadata(self):
        """Return a long description of the metadata of the layer."""
        return {}


class RasterLayer(Layer):

    # mimetype for a rasterlayer, the first mimetype is the one
    # chosen by default for exposing the file
    MIMETYPE = ["image/geotiff", "image/tiff"]
    _RASTER_NAME = "raster.tiff"
    FOLDER = "raster"

    @staticmethod
    def list_layers():
        """As we store rasters on disk, we only want to list
        files in the directory.
        """
        layers = os.listdir(get_geodb_subfolder(RasterLayer.FOLDER))
        non_hidden_layers = filter(lambda a: not a.startswith("."), layers)
        return map(RasterLayer, non_hidden_layers)

    @staticmethod
    def _get_file_fullpath(name):
        return safe_join(get_geodb_subfolder(RasterLayer.FOLDER), name)

    @staticmethod
    def _get_tmp_dir():
        return get_tmp_geodb_dir()

    def _get_raster_dir(self):
        """Return the path to the directory containing the raster path"""
        raster_dir = safe_join(get_geodb_subfolder(self.FOLDER), self.name)
        return raster_dir

    def _get_raster_path(self):
        """Return the path to the raster directory stored on disk."""
        layer_path = safe_join(self._get_raster_dir(), self._RASTER_NAME)
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
        with TemporaryDirectory(prefix=self._get_tmp_dir()) as tmp_dir:
            os.rename(self._get_raster_dir(), tmp_dir)
            shutil.rmtree(tmp_dir)

    @classmethod
    def save(cls, file_upload: FileStorage):
        """Save a FileStorage instance and return the RasterLayer instance.
        To do so,
        * the layer is saved in a temporary directory as tiff.
          -> path : /geodb/tmp/raster.tiff,
        * and then replace its in the raster directory.
          -> path : /geodb/{FOLDER}/(file_upload_filename)/raster.tiff.
          -> path : /cm_outputs/{FOLDER}/(file_upload_filename)/raster.tiff.

        An error is raised if the geofile already exists.
        """
        with TemporaryDirectory(prefix=cls._get_tmp_dir()) as tmp_dir:
            tmp_filepath = safe_join(tmp_dir, RasterLayer._RASTER_NAME)
            file_upload.save(tmp_filepath)
            output_filepath = cls._get_file_fullpath(file_upload.filename)
            os.makedirs(output_filepath, exist_ok=True)
            # replace will replace the file if it already exists, we should first check
            # if the file already exists before proceeding
            try:
                os.replace(tmp_dir, output_filepath)
            except (FileExistsError, OSError):
                print("Geofile already exists")
            # except FileExistsError:
            #     raise SaveException("Geofile already exists")
        return cls(file_upload.filename)

    def as_mapnik_layer(self):
        """Open the geofile as Mapnik layer."""
        # TODO: extract this from raster in advance
        layer = mapnik.Layer(self.name)
        layer_path = self._get_raster_path()
        layer.srs = self.projection
        # TODO: get this from the upload folder, check layer at that point ?
        gdal_source = mapnik.Gdal(file=layer_path, band=1)
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

    def exists(self):
        """Indicates if the file exists"""
        return os.path.exists(self._get_raster_path())


class CMRasterLayer(RasterLayer):
    @staticmethod
    def list_layers():
        """As we store rasters on disk, we only want to list
        files in the directory.
        """
        root_folder = current_app.config["CM_OUTPUTS_DIR"]

        layers = []
        for root, dirs, files in os.walk(root_folder):
            if files:
                _, name = os.path.split(root)
                layers.append(name)

        non_hidden_layers = filter(lambda a: not a.startswith("."), layers)

        return map(CMRasterLayer, non_hidden_layers)

    @staticmethod
    def _get_file_fullpath(name):
        parts = name.split("_")

        if parts[-1].find("-") >= 0:
            prefix = parts[-1].split("-")[0]
            parts = parts[:-1]

            for i in range(0, len(prefix), 2):
                parts.append(prefix[i : i + 2])

        parts.append(name)

        return safe_join(current_app.config["CM_OUTPUTS_DIR"], os.path.sep.join(parts))

    @staticmethod
    def _get_tmp_dir():
        return get_tmp_cm_outputs_dir()

    def _get_raster_dir(self):
        """Return the path to the directory containing the raster path"""
        return self._get_file_fullpath(self.name)

    def touch(self):
        """Sets the modification and access times of files to the current time of day"""
        Path(self._get_raster_path()).touch()


class VectorLayer(Layer):
    """Future implementation of a vector layer."""

    MIMETYPE = ["application/zip"]

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
        """Open the geofile as Mapnik layer."""
        layer = mapnik.Layer(self.name)
        shapefiles = glob(os.path.join(self._get_vector_dir(), "*.shp"))
        if not shapefiles:
            print("Shapefile was not found")
            # raise FileNotFoundError("Shapefile was not found")
        layer.srs = self.projection
        try:
            layer.datasource = mapnik.Shapefile(file=shapefiles[0])
        except IndexError:
            print("Shapefile error")
            raise
        layer.queryable = True
        return layer

    def _get_vector_dir(self):
        return safe_join(get_geodb_subfolder("vectors"), self.name)

    @property
    def projection(self):
        """Return the projection of the vector layer."""
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
        with TemporaryDirectory(prefix=get_tmp_geodb_dir()) as tmp_dir:
            zip_ref.extractall(tmp_dir)
            geodb_dir = get_geodb_subfolder("vectors")
            output_dirpath = safe_join(geodb_dir, file_upload.filename)
            try:
                os.replace(tmp_dir, output_dirpath)
            except FileExistsError:
                # raise SaveException("Geofile already exists")
                print("Geofile already exists")
        return VectorLayer(file_upload.filename)

    @staticmethod
    def list_layers():
        """List file in the vector directory
        Ignore hidden file as they are used for unzipping destination and don't
        provide ondisk consistency.
        """
        layers = os.listdir(get_geodb_subfolder("vectors"))
        non_hidden_layers = filter(lambda a: not a.startswith("."), layers)
        return map(VectorLayer, non_hidden_layers)

    def delete(self):
        """Here we do a little switcheroo to guarantee that the directory deletion is
        done atomically:
        1) Move the directory into a "to be deleted directory", this has atomicity
            guarantee as long as we move inside the same filesystem
        2) Run shutil.rmtree, this operation could fail at any moment and leave
           remaining files around in the to_be_deleted_dir
        """
        with TemporaryDirectory(prefix=get_tmp_geodb_dir()) as tmp_dir:
            os.rename(self._get_vector_dir(), tmp_dir)
            shutil.rmtree(tmp_dir)

    def get_legend_images(self, legend_style):
        """Returns a list of the images corresponding to the colors needed by the
        legend. If the images don't exists, create them.
        """
        images_folder = safe_join(self._get_vector_dir(), "legend")
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        images = []
        for n, (color, min_threshold, max_threshold) in enumerate(legend_style):
            filename = safe_join(images_folder, f"{n:02}.png")
            if not os.path.exists(filename):
                img = Image.new("RGB", (4, 4), color=color)
                img.save(filename)

            images.append(filename)

        return images


class GeoJSONLayer(VectorLayer):
    """This is just a shim to the VectorLayer, we take a geojson as input in the
    save method, then transform it to a shapefile directory containing a proj file
    and a shp file.
    """

    MIMETYPE = ["application/json", "application/geojson", "application/geo+json"]
    DEFAULT_PROJECTION = epsg_to_wkt(4326)

    @staticmethod
    def list_layers():
        """This method doesn't store anything. All is done in Vector Layer."""
        return []

    @staticmethod
    def save(file_upload: FileStorage):
        """This method takes a geojson as input and present it as a raster file"""
        with TemporaryDirectory(prefix=get_tmp_geodb_dir()) as tmp_dir:
            tmp_filepath = safe_join(tmp_dir, file_upload.filename)
            file_upload.save(tmp_filepath)
            shape_name, _ = os.path.splitext(file_upload.filename)
            shapefile_filepath = safe_join(tmp_dir, shape_name + ".shp")
            args = ["ogr2ogr", "-f", "ESRI Shapefile", shapefile_filepath, tmp_filepath]
            try:
                # This call is safe, as
                # * we don't call a shell
                # * we always prepend the location, thus we end up with
                #   absolute path that don't start with - or --
                # * all joins are contained in the subdirectories
                subprocess.check_call(args)  # nosec
            except subprocess.CalledProcessError as e:
                print("File cannot be encoded into a shapefile")
                print(e)
                # raise SaveException("File cannot be encoded into a shapefile")

            proj_filepath = safe_join(tmp_dir, shape_name + ".prj")
            # geojson can use a single projection,
            # so create that file with the standard geojson projection
            with open(proj_filepath, "w") as fd:
                fd.write(GeoJSONLayer.DEFAULT_PROJECTION)
            os.remove(tmp_filepath)

            # everything went fine, symlink and return the corresponding VectorLayer
            geodb_dir = get_geodb_subfolder("vectors")
            output_dirpath = safe_join(geodb_dir, shape_name + ".geojson")
            try:
                os.replace(tmp_dir, output_dirpath)
            except (FileExistsError, OSError):
                print("Geofile already exists")
                # raise SaveException("Geofile already exists")
            except Exception as e:
                print(e)
        return VectorLayer(shape_name + ".geojson")
