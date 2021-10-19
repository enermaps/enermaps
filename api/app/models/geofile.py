"""Description of each set of gis informations.

Modification of layer are made quite slow, so we don't
really prevent race condition on list vs delete. We
also catch those on accessing the layer.

"""
import json
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp

import mapnik
from flask import safe_join
from PIL import Image

from app.common import path
from app.common.projection import proj4_from_geotiff  # epsg_to_proj4,
from app.common.projection import epsg_to_wkt, proj4_from_shapefile

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
            os.replace(tmp_dir, target_folder)
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
        subfolder = os.path.dirname(feature_id)
        if len(subfolder) > 0:
            os.makedirs(safe_join(tmp_dir, subfolder), exist_ok=True)

        tmp_filepath = safe_join(tmp_dir, feature_id)

        with open(tmp_filepath, "wb") as f:
            f.write(raster_content)

        target_folder = storage_instance.get_dir(layer_name)
        if len(subfolder) > 0:
            target_folder = safe_join(target_folder, subfolder)

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

    folder = storage_instance.get_dir(layer_name)
    if not os.path.exists(folder):
        return

    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        os.rename(folder, tmp_dir)
        shutil.rmtree(tmp_dir)


class Layer(ABC):
    """This is a base class for the layers.
    Each layer subclass have the set of method declared underneath.
    """

    def __init__(self, layer_name, storage):
        self.name = layer_name
        self.storage = storage

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


class VectorLayer(Layer):
    """Future implementation of a vector layer."""

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

    def get_legend_images(self, legend):
        """Create images containing the colors defined in the legend. The caller is
        responsible to delete the folder when the images aren't needed anymore.
        """
        images_folder = mkdtemp(prefix=self.storage.get_tmp_dir())

        images = []
        for index, symbol in enumerate(legend["symbology"]):
            color = (
                symbol["red"],
                symbol["green"],
                symbol["blue"],
                int(symbol["opacity"] * 255),
            )

            filename = safe_join(images_folder, f"{index:02}.png")

            img = Image.new("RGBA", (4, 4), color=color)
            img.save(filename)

            images.append(filename)

        return (images, images_folder)
