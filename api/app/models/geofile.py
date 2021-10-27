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
import ogr
import osr
from flask import current_app, safe_join
from PIL import Image

import app.common.projection as project
from app.common import path

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

    # Processing
    valid_variables = []

    filtered_features = []
    for i in range(len(geojson["features"])):
        feature = geojson["features"][i]

        if (
            ("geometry" in feature)
            and (feature["geometry"] is not None)
            and (len(feature["geometry"]["coordinates"]) == 0)
        ):
            break

        properties = feature["properties"]

        # Retrieve the list of variable names
        for variable, value in properties["variables"].items():
            if (variable not in valid_variables) and (value is not None):
                valid_variables.append(variable)

        # Delete the legend (we don't need it)
        del properties["legend"]

        # Add the variable values as keys accessible by mapnik
        for variable, value in properties["variables"].items():
            properties[f"__variable__{variable}"] = value

        filtered_features.append(feature)

    geojson["features"] = filtered_features

    # Save the files
    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        tmp_filepath = safe_join(tmp_dir, storage_instance.GEOJSON_FILENAME)
        proj_filepath = safe_join(tmp_dir, storage_instance.PROJECTION_FILENAME)
        variables_filepath = safe_join(tmp_dir, storage_instance.VARIABLES_FILENAME)

        with open(tmp_filepath, "w") as f:
            f.write(json.dumps(geojson))

        with open(proj_filepath, "w") as fd:
            fd.write(
                project.epsg_string_to_proj4(
                    current_app.config["VECTOR_PROJECTION_SYSTEM"]
                )
            )

        with open(variables_filepath, "w") as f:
            f.write(json.dumps(valid_variables))

        target_folder = storage_instance.get_dir(layer_name)
        os.makedirs(os.path.dirname(target_folder), exist_ok=True)

        try:
            os.replace(tmp_dir, target_folder)
        except (FileExistsError, OSError):
            print("Geofile already exists")
        except Exception as e:
            print(e)

    return valid_variables


def save_raster_projection(layer_name, projection):
    if (projection is None) or (projection == ""):
        return

    (type, id, _, _, _) = path.parse_unique_layer_name(layer_name)
    layer_name = path.make_unique_layer_name(type, id)

    storage_instance = storage.create_for_layer_type(type)

    # Save the file
    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        tmp_filepath = safe_join(tmp_dir, storage_instance.PROJECTION_FILENAME)

        with open(tmp_filepath, "w") as f:
            f.write(projection)

        target_filename = storage_instance.get_projection_file(layer_name)
        os.makedirs(os.path.dirname(target_filename), exist_ok=True)

        try:
            os.replace(tmp_filepath, target_filename)
        except (FileExistsError, OSError):
            print("Projection file already exists")
        except Exception as e:
            print(e)


def save_raster_geometries(layer_name, geojson):
    type = path.get_type(layer_name)
    storage_instance = storage.create_for_layer_type(type)

    # Ensure that there are some features
    if len(geojson["features"]) == 0:
        return

    # Processing
    geometries = {}

    for feature in geojson["features"]:
        geometry = feature["geometry"]

        if (geometry is None) or (geometry["type"] != "Polygon"):
            geometries[feature["id"]] = None
        else:
            geometries[feature["id"]] = geometry["coordinates"][0]

    # Save the file
    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        tmp_filepath = safe_join(tmp_dir, storage_instance.GEOMETRIES_FILENAME)

        with open(tmp_filepath, "w") as f:
            f.write(json.dumps(geometries))

        target_filename = storage_instance.get_geometries_file(layer_name)
        os.makedirs(os.path.dirname(target_filename), exist_ok=True)

        try:
            os.replace(tmp_filepath, target_filename)
        except (FileExistsError, OSError):
            print("Geometries file already exists")
        except Exception as e:
            print(e)


def save_raster_file(layer_name, feature_id, raster_content):
    storage_instance = storage.create_for_layer_type(path.RASTER)
    return _save_raster_file(storage_instance, layer_name, feature_id, raster_content)


def save_cm_file(layer_name, feature_id, raster_content):
    storage_instance = storage.create_for_layer_type(path.CM)
    return _save_raster_file(storage_instance, layer_name, feature_id, raster_content)


def save_cm_result(layer_name, result):
    return _save_cm_json(layer_name, "result.json", result)


def save_cm_parameters(layer_name, parameters):
    return _save_cm_json(layer_name, "parameters.json", parameters)


def get_cm_legend(layer_name):
    storage_instance = storage.create_for_layer_type(path.CM)

    filename = storage_instance.get_file_path(layer_name, "result.json")
    if not os.path.exists(filename):
        return None

    with open(filename, "r") as f:
        result = json.load(f)

    if "legend" in result:
        return result["legend"]

    return None


def _save_raster_file(storage_instance, layer_name, feature_id, raster_content):
    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        subfolder = os.path.dirname(feature_id)
        if len(subfolder) > 0:
            os.makedirs(safe_join(tmp_dir, subfolder), exist_ok=True)

        tmp_filepath = safe_join(tmp_dir, feature_id)

        with open(tmp_filepath, "wb") as f:
            f.write(raster_content)

        # For CMs: extract the projection form the raster file
        proj_filepath = None
        if path.get_type(layer_name) == path.CM:
            projection = project.proj4_from_geotiff(tmp_filepath)
            if projection is None:
                return False

            proj_filepath = tmp_filepath.replace(".tif", ".prj")
            with open(proj_filepath, "w") as f:
                f.write(projection)

        target_folder = storage_instance.get_dir(layer_name)
        if len(subfolder) > 0:
            target_folder = safe_join(target_folder, subfolder)

        os.makedirs(target_folder, exist_ok=True)

        try:
            os.replace(
                tmp_filepath, storage_instance.get_file_path(layer_name, feature_id)
            )

            if proj_filepath is not None:
                os.replace(
                    proj_filepath,
                    storage_instance.get_projection_file(layer_name, feature_id),
                )
        except (FileExistsError, OSError):
            print("Raster file already exists")
            return False
        except Exception as e:
            print(e)
            return False

    return True


def _save_cm_json(layer_name, filename, data):
    storage_instance = storage.create_for_layer_type(path.CM)

    with TemporaryDirectory(prefix=storage_instance.get_tmp_dir()) as tmp_dir:
        tmp_filepath = safe_join(tmp_dir, filename)

        with open(tmp_filepath, "w") as f:
            json.dump(data, f)

        target_folder = storage_instance.get_dir(layer_name)
        os.makedirs(target_folder, exist_ok=True)

        try:
            os.replace(
                tmp_filepath, storage_instance.get_file_path(layer_name, filename)
            )
        except Exception as e:
            print(e)
            return False

    return True


def delete_all_features(layer_name):
    storage_instance = storage.create(layer_name)

    folder = storage_instance.get_dir(layer_name, cache=True)
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
    def as_mapnik_layers(self, bbox=None, bbox_projection=None):
        """Return the Layer as a list of mapnik layers
        (https://mapnik.org/docs/v2.2.0/api/python/mapnik._mapnik.Layer-class.html)
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

    def as_mapnik_layers(self, bbox=None, bbox_projection=None):
        """Open the geofile as Mapnik layer."""

        # Only use as many raster files as necessary
        rasters = self.get_rasters_in_bbox(bbox, bbox_projection)

        type = path.get_type(self.name)

        if type == path.RASTER:
            projection = self.storage.get_projection(self.name)

            # By security
            if projection is None:
                projection = project.epsg_string_to_proj4(
                    current_app.config["RASTER_PROJECTION_SYSTEM"]
                )

        layers = []
        for feature_id, raster_path in rasters:
            layer = mapnik.Layer(feature_id)
            layer.datasource = mapnik.Gdal(file=raster_path, band=1)
            layer.queryable = False

            if type == path.RASTER:
                layer.srs = projection
            elif type == path.CM:
                layer.srs = self.storage.get_projection(self.name, feature_id)

            layers.append(layer)

            # For CM results: sets the modification and access times of files to the
            # current time of day
            if type == path.CM:
                Path(raster_path).touch()

        return layers

    def get_rasters_in_feature_list(self, features):
        geometries = self.storage.get_geometries(self.name)

        rasters = []

        # No geometry file
        if geometries is None:
            for feature_id in self.storage.list_feature_ids(self.name):
                rasters.append(
                    (feature_id, self.storage.get_file_path(self.name, feature_id))
                )
            return rasters

        # No polygon in the geometry file
        if geometries[next(iter(geometries))] is None:
            for feature_id in geometries.keys():
                rasters.append(
                    (feature_id, self.storage.get_file_path(self.name, feature_id))
                )
            return rasters

        # Check the intersections
        polygons = []

        for feature in features:
            for coordinates in feature["geometry"]["coordinates"]:
                ring = ogr.Geometry(ogr.wkbLinearRing)

                for p in coordinates:
                    ring.AddPoint(p[0], p[1])

                poly = ogr.Geometry(ogr.wkbPolygon)
                poly.AddGeometry(ring)

                polygons.append(poly)

        return self._get_rasters_in_polygons(geometries, polygons)

    def get_rasters_in_bbox(self, bbox, bbox_projection):
        geometries = self.storage.get_geometries(self.name)

        rasters = []

        # No geometry file
        if geometries is None:
            for feature_id in self.storage.list_feature_ids(self.name):
                rasters.append(
                    (feature_id, self.storage.get_file_path(self.name, feature_id))
                )
            return rasters

        # No polygon in the geometry file
        if (
            (bbox is None)
            or (bbox_projection is None)
            or (geometries[next(iter(geometries))] is None)
        ):
            for feature_id in geometries.keys():
                rasters.append(
                    (feature_id, self.storage.get_file_path(self.name, feature_id))
                )
            return rasters

        # Check the intersections
        source_ref = osr.SpatialReference()
        target_ref = osr.SpatialReference()

        source_ref.ImportFromEPSG(project.epsg_string_to_epsg(bbox_projection))
        target_ref.ImportFromEPSG(
            project.epsg_string_to_epsg(current_app.config["RASTER_PROJECTION_SYSTEM"])
        )

        t = osr.CoordinateTransformation(source_ref, target_ref)

        bbox_top_left = t.TransformPoint(bbox.minx, bbox.maxy)
        bbox_bottom_right = t.TransformPoint(bbox.maxx, bbox.miny)

        bbox_ring = ogr.Geometry(ogr.wkbLinearRing)
        bbox_ring.AddPoint(bbox_top_left[1], bbox_top_left[0])
        bbox_ring.AddPoint(bbox_top_left[1], bbox_bottom_right[0])
        bbox_ring.AddPoint(bbox_bottom_right[1], bbox_bottom_right[0])
        bbox_ring.AddPoint(bbox_bottom_right[1], bbox_top_left[0])
        bbox_ring.AddPoint(bbox_top_left[1], bbox_top_left[0])

        bbox_poly = ogr.Geometry(ogr.wkbPolygon)
        bbox_poly.AddGeometry(bbox_ring)

        return self._get_rasters_in_polygons(geometries, [bbox_poly])

    def _get_rasters_in_polygons(self, geometries, polygons):
        rasters = []

        for feature_id, coordinates in geometries.items():
            raster_ring = ogr.Geometry(ogr.wkbLinearRing)

            for p in coordinates:
                raster_ring.AddPoint(p[0], p[1])

            raster_poly = ogr.Geometry(ogr.wkbPolygon)
            raster_poly.AddGeometry(raster_ring)

            for polygon in polygons:
                intersection = polygon.Intersection(raster_poly)
                if intersection.GetGeometryCount() > 0:
                    rasters.append(
                        (feature_id, self.storage.get_file_path(self.name, feature_id))
                    )
                    break

        return rasters


class VectorLayer(Layer):
    """Future implementation of a vector layer."""

    def as_mapnik_layers(self, bbox=None, bbox_projection=None):
        geojson_file = self.storage.get_geojson_file(self.name)
        if not os.path.exists(geojson_file):
            print(f"GeoJSON file '{geojson_file}' was not found")
            return None

        projection = self.storage.get_projection(self.name)

        # By security
        if projection is None:
            projection = project.epsg_string_to_proj4(
                current_app.config["VECTOR_PROJECTION_SYSTEM"]
            )

        layer = mapnik.Layer(self.name)
        layer.datasource = mapnik.GeoJSON(file=geojson_file)
        layer.srs = projection
        layer.queryable = True

        return [layer]

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
                int(symbol["red"]),
                int(symbol["green"]),
                int(symbol["blue"]),
                int(symbol["opacity"] * 255),
            )

            filename = safe_join(images_folder, f"{index:02}.png")

            img = Image.new("RGBA", (4, 4), color=color)
            img.save(filename)

            images.append(filename)

        return (images, images_folder)
