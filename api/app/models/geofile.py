"""Description of each set of gis informations.

Modification of layer are made quite slow, so we don't
really prevent race condition on list vs delete. We
also catch those on accessing the layer.

"""
import io
import json
import os
import shutil
import zipfile
from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import TemporaryDirectory

import mapnik
from app.common import path
from app.common.projection import proj4_from_geotiff  # epsg_to_proj4,
from app.common.projection import epsg_to_wkt, proj4_from_shapefile
from flask import safe_join
from PIL import Image

from . import storage


def load(name):
    """Create a new instance of RasterLayer based on its name"""
    type = path.get_type(name)
    storage_instance = storage.create_for_layer_type(type)

    if type in (path.AREA, path.VECTOR):
        return VectorLayer(name, storage_instance)
    else:
        return RasterLayer(name, storage_instance)

    return None


def save_vector_geojson(layer_name, geojson):
    type = path.get_type(layer_name)
    storage_instance = storage.create_for_layer_type(type)

    # Add the variable names as keys accessible by mapnik
    for i in range(len(geojson["features"])):
        for variable, value in geojson["features"][i]["properties"][
            "variables"
        ].items():
            geojson["features"][i]["properties"][f"__variable__{variable}"] = value

    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        tmp_filepath = safe_join(tmp_dir, "data.geojson")
        proj_filepath = safe_join(tmp_dir, "data.prj")

        with open(tmp_filepath, "w") as f:
            f.write(json.dumps(geojson))

        with open(proj_filepath, "w") as fd:
            fd.write(epsg_to_wkt(4326))

        target_folder = storage_instance.get_dir(layer_name)
        os.makedirs(os.path.dirname(target_folder), exist_ok=True)

        try:
            os.replace(tmp_dir, storage_instance.get_dir(layer_name))
        except (FileExistsError, OSError):
            print("Geofile already exists")
        except Exception as e:
            print(e)

    return True


def save_raster_file(layer_name, feature_id, raster_content):
    storage_instance = storage.create_for_layer_type(path.RASTER)
    return _save_raster_file(storage_instance, layer_name, feature_id, raster_content)


def save_cm_file(layer_name, feature_id, raster_content):
    storage_instance = storage.create_for_layer_type(path.CM)
    return _save_raster_file(storage_instance, layer_name, feature_id, raster_content)


def _save_raster_file(storage_instance, layer_name, feature_id, raster_content):
    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        tmp_filepath = safe_join(tmp_dir, feature_id)

        with open(tmp_filepath, "wb") as f:
            f.write(raster_content)

        target_folder = storage_instance.get_dir(layer_name)
        os.makedirs(target_folder, exist_ok=True)

        try:
            os.replace(
                tmp_filepath, storage_instance.get_file_path(layer_name, feature_id)
            )
        except (FileExistsError, OSError):
            print("Raster file already exists")
            return False
        except Exception as e:
            print(e)
            return False

    return True


def delete_all_features(layer_name):
    storage_instance = storage.create(layer_name)

    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        os.rename(storage_instance.get_dir(layer_name), tmp_dir)
        shutil.rmtree(tmp_dir)


class Layer(ABC):
    """This is a baseclass for the layers
    Each layer subclass have the set of method declared underneath.
    Each layer subclass also has a MIMETYPE constant which is a list
    of string mimetype. The first index of that array is the default
    mimetype of that layer used upon retrieving that layer.
    """

    def __init__(self, layer_name, storage):
        self.name = layer_name
        self.storage = storage

    @abstractmethod
    def as_fd(self):
        """Return the Layer as an open file descriptor.

        A warning here, the closing of the file descriptor is left for the
        callee.
        """
        pass

    @abstractmethod
    def as_mapnik_layers(self):
        """Return the Layer as a list of mapnik layers
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


class RasterLayer(Layer):
    @property
    def is_queryable(self):
        return False

    @property
    def projection(self):
        """Return the projection of the raster layer,
        currently this approach is quite naive as we read
        from the disk to only extract the projection.
        """
        try:
            return proj4_from_geotiff(
                self.storage.get_file_path(
                    self.name, self.storage.list_feature_ids(self.name)[0]
                )
            )
        except Exception:
            return None

    def as_mapnik_layers(self):
        """Open the geofile as Mapnik layer."""
        layers = []

        for feature_id in self.storage.list_feature_ids(self.name):
            layer_path = self.storage.get_file_path(self.name, feature_id)

            layer = mapnik.Layer(feature_id)
            layer.datasource = mapnik.Gdal(file=layer_path, band=1)
            layer.srs = self.projection
            layer.queryable = False

            layers.append(layer)

            # For CM results: sets the modification and access times of files to the
            # current time of day
            if path.get_type(self.name) == path.CM:
                Path(layer_path).touch()

        return layers

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

    def as_mapnik_layers(self):
        geojson_file = self.storage.get_geojson_file(self.name)
        if not os.path.exists(geojson_file):
            print(f"GeoJSON file '{geojson_file}' was not found")
            return None

        layer = mapnik.Layer(self.name)
        layer.srs = self.projection
        layer.datasource = mapnik.GeoJSON(file=geojson_file)
        layer.queryable = True

        return [layer]

    @property
    def projection(self):
        """Return the projection of the vector layer."""
        try:
            return proj4_from_shapefile(self.storage.get_dir(self.name))
        except Exception:
            return None

    @property
    def is_queryable(self):
        """Return true if the layer has features, this allow the layer to be
        queried for feature at a given location
        """
        return True

    def get_legend_images(self, legend_style):
        """Returns a list of the images corresponding to the colors needed by the
        legend. If the images don't exists, create them.
        """
        images_folder = safe_join(self.storage.get_dir(self.name), "legend")
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
