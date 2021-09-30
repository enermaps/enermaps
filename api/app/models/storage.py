import os

from flask import current_app, safe_join


class GeoDBRasterStorage(object):
    def get_root_dir(self):
        if current_app.config["GEODB_DIR"] is not None:
            return current_app.config["GEODB_DIR"]

        return safe_join(current_app.config["GEODB_CACHE_DIR"], "rasters")

    def get_tmp_dir(self):
        return safe_join(current_app.config["GEODB_CACHE_DIR"], "tmp")

    def get_dir(self, id):
        return safe_join(self.get_root_dir(), str(id))

    def get_file_path(self, id, layer_name):
        return safe_join(self.get_dir(id), layer_name)


class CMOutputStorage(object):
    def get_root_dir(self):
        return safe_join(current_app.config["CM_OUTPUTS_DIR"])

    def get_tmp_dir(self):
        return safe_join(current_app.config["CM_OUTPUTS_DIR"], "tmp")

    def get_dir(self, id):
        parts = id.split("_")

        if parts[-1].find("-") >= 0:
            prefix = parts[-1].split("-")[0]
            parts = parts[:-1]

            for i in range(0, min(len(prefix), 6), 2):
                parts.append(prefix[i : i + 2])

        parts.append(id)

        return safe_join(self.get_root_dir(), os.path.sep.join(parts))

    def get_file_path(self, id, layer_name):
        return safe_join(self.get_dir(id), layer_name)


class GeoDBVectorStorage(object):
    def get_root_dir(self):
        return safe_join(current_app.config["GEODB_CACHE_DIR"], "vectors")

    def get_tmp_dir(self):
        return safe_join(current_app.config["GEODB_CACHE_DIR"], "tmp")

    def get_dir(self, id):
        return safe_join(self.get_root_dir(), str(id))

    def get_file_path(self, id, layer_name):
        return safe_join(self.get_dir(id), layer_name)
