import glob
import json
import os

from app.common import path
from flask import current_app, safe_join


def create(layer_name):
    return create_for_layer_type(path.get_type(layer_name))


def create_for_layer_type(type):
    if type == path.AREA:
        return AreaStorage()
    elif type == path.VECTOR:
        return VectorStorage()
    elif type == path.RASTER:
        return RasterStorage()
    elif type == path.CM:
        return CMStorage()

    return None


class BaseRasterStorage(object):
    def get_root_dir(self):
        raise NotImplementedError

    def get_tmp_dir(self):
        raise NotImplementedError

    def get_dir(self, layer_name):
        raise NotImplementedError

    def get_file_path(self, layer_name, feature_id):
        return safe_join(self.get_dir(layer_name), feature_id)

    def list_feature_ids(self, layer_name):
        folder = self.get_dir(layer_name)
        return [
            x[len(folder) + 1 :]
            for x in glob.glob(safe_join(folder, "**/*.tif"), recursive=True)
        ]

    def get_geometries(self, layer_name):
        filename = self.get_file_path(layer_name, "geometries.json")
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return json.load(f)


class RasterStorage(BaseRasterStorage):
    def get_root_dir(self):
        if current_app.config["RASTER_CACHE_DIR"] is not None:
            return current_app.config["RASTER_CACHE_DIR"]

        return safe_join(current_app.config["WMS_CACHE_DIR"], "rasters")

    def get_tmp_dir(self):
        return safe_join(current_app.config["WMS_CACHE_DIR"], "tmp")

    def get_dir(self, layer_name):
        if current_app.config["RASTER_CACHE_DIR"] is not None:
            (_, id, _, _, _) = path.parse_unique_layer_name(layer_name)
            return safe_join(self.get_root_dir(), str(id))
        else:
            return safe_join(self.get_root_dir(), path.to_folder_path(layer_name))


class CMStorage(BaseRasterStorage):
    def get_root_dir(self):
        return safe_join(current_app.config["CM_OUTPUTS_DIR"])

    def get_tmp_dir(self):
        return safe_join(current_app.config["CM_OUTPUTS_DIR"], "tmp")

    def get_dir(self, layer_name):
        return safe_join(self.get_root_dir(), path.to_folder_path(layer_name))


class BaseVectorStorage(object):
    def get_root_dir(self):
        raise NotImplementedError

    def get_tmp_dir(self):
        return safe_join(current_app.config["WMS_CACHE_DIR"], "tmp")

    def get_dir(self, layer_name):
        return safe_join(self.get_root_dir(), path.to_folder_path(layer_name))

    def get_file_path(self, layer_name, extension):
        return safe_join(self.get_dir(layer_name), f"data.{extension}")

    def get_geojson_file(self, layer_name):
        return self.get_file_path(layer_name, "geojson")


class VectorStorage(BaseVectorStorage):
    def get_root_dir(self):
        return safe_join(current_app.config["WMS_CACHE_DIR"], "vectors")


class AreaStorage(BaseVectorStorage):
    def get_root_dir(self):
        return safe_join(current_app.config["WMS_CACHE_DIR"], "areas")
