"""Functions related to the "GetCapabilities" operation of the Web Map Service (WMS)"""

import itertools
import os

import osr
from flask import current_app, request
from lxml import etree  # nosec

import app.common.projection as project
from app.common import client
from app.common import datasets as datasets_fcts
from app.common import path, xml
from app.models import storage

current_file_dir = os.path.dirname(os.path.abspath(__file__))


def get_capabilities():
    """Return an xml description of the capabilities of the current WMS
    set of endpoints.

    This method starts with a preexisting XML template, parses it then
    insert dynamic element from the list of layers and from the flask
    configuration.
    """
    with open(os.path.join(current_file_dir, "capabilities.xml"), "rb") as f:
        root = xml.etree_fromstring(f.read())

    root_layer = root.find("Capability/Layer", root.nsmap)

    layer_name = etree.Element("Name")
    root_layer.insert(0, layer_name)

    layer_title = etree.Element("Title")
    root_layer.insert(1, layer_title)

    for crs in current_app.config["WMS"]["ALLOWED_PROJECTIONS"]:
        crs_node = etree.Element("CRS")
        crs_node.text = crs.upper()
        root_layer.insert(2, crs_node)

    capabilities = root.findall("Capability//OnlineResource", root.nsmap)
    capabilities += root.findall("Service//OnlineResource", root.nsmap)
    for element in capabilities:
        element.set("{http://www.w3.org/1999/xlink}href", request.base_url)

    get_map = root.find("Capability/Request/GetMap", root.nsmap)
    for get_map_format in current_app.config["WMS"]["GETMAP"]["ALLOWED_OUTPUTS"]:
        format_node = etree.Element("Format")
        format_node.text = get_map_format
        get_map.insert(0, format_node)

    datasets = client.get_dataset_list()
    if len(datasets) == 0:
        return None

    for dataset in datasets:
        type = path.RASTER if dataset["is_raster"] else path.VECTOR

        layer_node = etree.Element("Layer")
        layer_node.set("queryable", "0" if dataset["is_raster"] else "1")
        layer_node.set("opaque", "0")

        title_node = etree.Element("Title")
        title_node.text = dataset["title"]
        layer_node.append(title_node)

        abstract = etree.Element("Abstract")
        layer_node.append(abstract)

        keyword_list = etree.Element("KeywordList")
        layer_node.append(keyword_list)

        for crs in current_app.config["WMS"]["ALLOWED_PROJECTIONS"]:
            crs_node = etree.Element("CRS")
            crs_node.text = crs.upper()
            layer_node.append(crs_node)

        parameters = client.get_parameters(dataset["ds_id"])
        if parameters is None:
            return None

        datasets_fcts.process_parameters(
            parameters,
            dataset_id=dataset["ds_id"],
            is_raster=dataset["is_raster"],
        )

        if (len(parameters["variables"]) > 0) and (len(parameters["time_periods"]) > 0):
            for variable, time_period in itertools.product(
                parameters["variables"], parameters["time_periods"]
            ):
                get_layer_capabilities(
                    layer_node,
                    dataset,
                    parameters,
                    type,
                    dataset["ds_id"],
                    variable=variable,
                    time_period=time_period,
                )
        elif len(parameters["variables"]) > 0:
            for variable in parameters["variables"]:
                get_layer_capabilities(
                    layer_node,
                    dataset,
                    parameters,
                    type,
                    dataset["ds_id"],
                    variable=variable,
                )
        elif len(parameters["time_periods"]) > 0:
            for time_period in parameters["time_periods"]:
                get_layer_capabilities(
                    layer_node,
                    dataset,
                    parameters,
                    type,
                    dataset["ds_id"],
                    time_period=time_period,
                )
        else:
            get_layer_capabilities(
                layer_node, dataset, parameters, type, dataset["ds_id"]
            )

        root_layer.append(layer_node)

    etree.indent(root, space="    ")

    return etree.tostring(root, pretty_print=True)


def get_layer_capabilities(
    parent_layer, dataset, parameters, type, id, variable=None, time_period=None
):
    layer_name = path.make_unique_layer_name(
        type, id, variable=variable, time_period=time_period
    )

    storage_instance = storage.create_for_layer_type(type)
    if not os.path.exists(storage_instance.get_dir(layer_name, cache=True)):
        return

    bbox = storage_instance.get_bbox(layer_name)
    if bbox is None:
        return

    sublayer_node = etree.Element("Layer")
    sublayer_node.set("queryable", "0" if dataset["is_raster"] else "1")
    sublayer_node.set("opaque", "0")

    title_node = etree.Element("Title")

    if (variable is not None) and (time_period is not None):
        title_node.text = dataset["title"] + " / " + variable + " / " + str(time_period)
    elif variable is not None:
        title_node.text = dataset["title"] + " / " + variable
    elif time_period is not None:
        title_node.text = dataset["title"] + " / " + str(time_period)
    else:
        title_node.text = dataset["title"]

    sublayer_node.append(title_node)

    name_node = etree.Element("Name")
    name_node.text = layer_name
    sublayer_node.append(name_node)

    projected_bbox = etree.Element("EX_GeographicBoundingBox")

    west_bound = etree.Element("westBoundLongitude")
    west_bound.text = str(bbox["left"])
    projected_bbox.append(west_bound)

    east_bound = etree.Element("eastBoundLongitude")
    east_bound.text = str(bbox["right"])
    projected_bbox.append(east_bound)

    south_bound = etree.Element("southBoundLatitude")
    south_bound.text = str(bbox["bottom"])
    projected_bbox.append(south_bound)

    north_bound = etree.Element("northBoundLatitude")
    north_bound.text = str(bbox["top"])
    projected_bbox.append(north_bound)

    sublayer_node.append(projected_bbox)

    zoom_limits = parameters.get("zoom_limits", {})
    if zoom_limits.get(layer_name, False):
        min_scale_denominator = etree.Element("MinScaleDenominator")
        min_scale_denominator.text = "2e6"
        sublayer_node.append(min_scale_denominator)

    source_ref = osr.SpatialReference()
    source_ref.ImportFromEPSG(
        project.epsg_string_to_epsg(current_app.config["VECTOR_PROJECTION_SYSTEM"])
    )

    for crs in current_app.config["WMS"]["ALLOWED_PROJECTIONS"]:
        bbox_node = etree.Element("BoundingBox")

        target_ref = osr.SpatialReference()
        target_ref.ImportFromEPSG(project.epsg_string_to_epsg(crs))

        t = osr.CoordinateTransformation(source_ref, target_ref)

        # In WMS 1.3.0, the order of parameters for BBOX depends on whether the CRS
        # definition has flipped axes. This is the case for "EPSG:4326" and "EPSG:3035".
        if current_app.config["VECTOR_PROJECTION_SYSTEM"] in ("EPSG:4326", "EPSG:3035"):
            bottom_left = t.TransformPoint(bbox["bottom"], bbox["left"])
            top_right = t.TransformPoint(bbox["top"], bbox["right"])
        else:
            bottom_left = t.TransformPoint(bbox["left"], bbox["bottom"])
            top_right = t.TransformPoint(bbox["right"], bbox["top"])

        bbox_node.set("minx", str(bottom_left[0]))
        bbox_node.set("maxx", str(top_right[0]))
        bbox_node.set("miny", str(bottom_left[1]))
        bbox_node.set("maxy", str(top_right[1]))

        bbox_node.set("CRS", crs)
        sublayer_node.append(bbox_node)

    parent_layer.append(sublayer_node)
