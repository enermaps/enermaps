import glob
import os

from flask import current_app, safe_join

from app.common import path


def create(layer_name):
    return create_for_layer_type(path.get_type(layer_name))


def create_for_layer_type(type):
    if type == path.AREA:
        return AreaStorage()
    elif type == path.VECTOR:
        return GeoDBVectorStorage()
    elif type == path.RASTER:
        return GeoDBRasterStorage()
    elif type == path.CM:
        return CMOutputStorage()

    return None


class GeoDBRasterStorage(object):
    def get_root_dir(self):
        if current_app.config["GEODB_DIR"] is not None:
            return current_app.config["GEODB_DIR"]

        return safe_join(current_app.config["GEODB_CACHE_DIR"], "rasters")

    def get_tmp_dir(self):
        return safe_join(current_app.config["GEODB_CACHE_DIR"], "tmp")

    def get_dir(self, layer_name):
        if current_app.config["GEODB_DIR"] is not None:
            (_, id, _, _) = path.parse_unique_layer_name(layer_name)
            return safe_join(self.get_root_dir(), str(id))
        else:
            return safe_join(self.get_root_dir(), path.to_folder_path(layer_name))

    def get_file_path(self, layer_name, feature_id):
        return safe_join(self.get_dir(layer_name), feature_id)

    def list_feature_ids(self, layer_name):
        folder = self.get_dir(layer_name)
        return [x[len(folder) + 1 :] for x in glob.glob(safe_join(folder, "*.tif"))]


class CMOutputStorage(object):
    def get_root_dir(self):
        return safe_join(current_app.config["CM_OUTPUTS_DIR"])

    def get_tmp_dir(self):
        return safe_join(current_app.config["CM_OUTPUTS_DIR"], "tmp")

    def get_dir(self, layer_name):
        folder_path = path.to_folder_path(layer_name)

        parts = folder_path.split("_")

        if parts[-1].find("-") >= 0:
            prefix = parts[-1].split("-")[0]
            parts = parts[:-1]

            for i in range(0, min(len(prefix), 6), 2):
                parts.append(prefix[i : i + 2])

        parts.append(folder_path)

        return safe_join(self.get_root_dir(), os.path.sep.join(parts))

    def get_file_path(self, layer_name, feature_id):
        return safe_join(self.get_dir(layer_name), feature_id)


class BaseVectorStorage(object):
    def get_root_dir(self):
        raise NotImplementedError

    def get_tmp_dir(self):
        return safe_join(current_app.config["GEODB_CACHE_DIR"], "tmp")

    def get_dir(self, layer_name):
        return safe_join(self.get_root_dir(), path.to_folder_path(layer_name))

    def get_file_path(self, layer_name, extension):
        return safe_join(self.get_dir(layer_name), f"data.{extension}")

    def get_geojson_file(self, layer_name):
        return self.get_file_path(layer_name, "geojson")


class GeoDBVectorStorage(BaseVectorStorage):
    def get_root_dir(self):
        return safe_join(current_app.config["GEODB_CACHE_DIR"], "vectors")


class AreaStorage(BaseVectorStorage):
    def get_root_dir(self):
        return safe_join(current_app.config["GEODB_CACHE_DIR"], "areas")
