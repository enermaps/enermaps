import glob
import json
import os

from flask import current_app, safe_join

from app.common import path


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

    PROJECTION_FILENAME = "projection.txt"
    GEOMETRIES_FILENAME = "geometries.json"
    BBOX_FILENAME = "bbox.json"

    def get_root_dir(self, cache=False):
        raise NotImplementedError

    def get_tmp_dir(self):
        raise NotImplementedError

    def get_dir(self, layer_name, cache=False):
        raise NotImplementedError

    def get_file_path(self, layer_name, feature_id):
        return safe_join(self.get_dir(layer_name), feature_id)

    def list_feature_ids(self, layer_name):
        folder = self.get_dir(layer_name)
        return [
            x[len(folder) + 1 :]
            for x in glob.glob(safe_join(folder, "**/*.tif"), recursive=True)
        ]

    def get_projection_file(self, layer_name):
        (_, id, _, _, _) = path.parse_unique_layer_name(layer_name)
        return safe_join(
            self.get_root_dir(cache=True),
            str(id),
            BaseRasterStorage.PROJECTION_FILENAME,
        )

    def get_geometries_file(self, layer_name):
        return safe_join(
            self.get_dir(layer_name, cache=True), BaseRasterStorage.GEOMETRIES_FILENAME
        )

    def get_bbox_file(self, layer_name):
        return safe_join(
            self.get_dir(layer_name, cache=True), BaseRasterStorage.BBOX_FILENAME
        )

    def get_geometries(self, layer_name):
        filename = self.get_geometries_file(layer_name)
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return json.load(f)

    def get_projection(self, layer_name):
        filename = self.get_projection_file(layer_name)
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return f.read()

    def get_bbox(self, layer_name):
        filename = self.get_bbox_file(layer_name)
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return json.load(f)


class RasterStorage(BaseRasterStorage):
    def get_root_dir(self, cache=False):
        if not (cache) and (current_app.config["RASTER_CACHE_DIR"] is not None):
            return current_app.config["RASTER_CACHE_DIR"]

        return safe_join(current_app.config["WMS_CACHE_DIR"], "rasters")

    def get_tmp_dir(self):
        return safe_join(current_app.config["WMS_CACHE_DIR"], "tmp")

    def get_dir(self, layer_name, cache=False):
        if not (cache) and (current_app.config["RASTER_CACHE_DIR"] is not None):
            (_, id, _, _, _) = path.parse_unique_layer_name(layer_name)
            return safe_join(self.get_root_dir(), str(id))
        else:
            return safe_join(
                self.get_root_dir(cache=cache), path.to_folder_path(layer_name)
            )


class CMStorage(BaseRasterStorage):
    def get_root_dir(self, cache=False):
        return safe_join(current_app.config["CM_OUTPUTS_DIR"])

    def get_tmp_dir(self):
        return safe_join(current_app.config["CM_OUTPUTS_DIR"], "tmp")

    def get_dir(self, layer_name, cache=False):
        return safe_join(self.get_root_dir(), path.to_folder_path(layer_name))

    def get_projection_file(self, layer_name, feature_id):
        return safe_join(self.get_dir(layer_name), feature_id.replace(".tif", ".prj"))

    def get_projection(self, layer_name, feature_id):
        filename = self.get_projection_file(layer_name, feature_id)
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return f.read()


class BaseVectorStorage(object):

    GEOJSON_FILENAME = "data.geojson"
    PROJECTION_FILENAME = "projection.txt"
    VARIABLES_FILENAME = "variables.json"
    COMBINATIONS_FILENAME = "combinations.json"
    BBOX_FILENAME = "bbox.json"

    def get_root_dir(self, cache=False):
        raise NotImplementedError

    def get_tmp_dir(self):
        return safe_join(current_app.config["WMS_CACHE_DIR"], "tmp")

    def get_dir(self, layer_name, cache=False):
        return safe_join(self.get_root_dir(), path.to_folder_path(layer_name))

    def get_file_path(self, layer_name, filename):
        return safe_join(self.get_dir(layer_name), filename)

    def get_geojson_file(self, layer_name):
        return self.get_file_path(layer_name, BaseVectorStorage.GEOJSON_FILENAME)

    def get_projection_file(self, layer_name):
        return self.get_file_path(layer_name, BaseVectorStorage.PROJECTION_FILENAME)

    def get_variables_file(self, layer_name):
        return self.get_file_path(layer_name, BaseVectorStorage.VARIABLES_FILENAME)

    def get_combinations_file(self, layer_name):
        return self.get_file_path(layer_name, BaseVectorStorage.COMBINATIONS_FILENAME)

    def get_bbox_file(self, layer_name):
        return self.get_file_path(layer_name, BaseVectorStorage.BBOX_FILENAME)

    def get_projection(self, layer_name):
        filename = self.get_projection_file(layer_name)
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return f.read()

    def get_combinations(self, layer_name):
        filename = self.get_combinations_file(layer_name)
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return json.load(f)

    def get_bbox(self, layer_name):
        filename = self.get_bbox_file(layer_name)
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return json.load(f)


class VectorStorage(BaseVectorStorage):
    def get_root_dir(self, cache=False):
        return safe_join(current_app.config["WMS_CACHE_DIR"], "vectors")


class AreaStorage(BaseVectorStorage):
    def get_root_dir(self, cache=False):
        return safe_join(current_app.config["WMS_CACHE_DIR"], "areas")
