"""Functions related to the "GetCapabilities" operation of the Web Map Service (WMS)"""

import itertools
import os

import mapnik
from flask import current_app, request
from lxml import etree  # nosec

from app.common import client, path, projection, xml
from app.models import geofile

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

        variables = client.get_variables(dataset["ds_id"])

        if (len(variables["variables"]) > 0) and (len(variables["time_periods"]) > 0):
            for variable, time_period in itertools.product(
                variables["variables"], variables["time_periods"]
            ):
                get_layer_capabilities(
                    layer_node,
                    dataset,
                    type,
                    dataset["ds_id"],
                    variable=variable,
                    time_period=time_period,
                )
        elif len(variables["variables"]) > 0:
            for variable in variables["variables"]:
                get_layer_capabilities(
                    layer_node, dataset, type, dataset["ds_id"], variable=variable
                )
        elif len(variables["time_periods"]) > 0:
            for time_period in variables["time_periods"]:
                get_layer_capabilities(
                    layer_node, dataset, type, dataset["ds_id"], time_period=time_period
                )
        else:
            get_layer_capabilities(layer_node, dataset, type, dataset["ds_id"])

        root_layer.append(layer_node)

    etree.indent(root, space="    ")

    return etree.tostring(root, pretty_print=True)


def get_layer_capabilities(
    parent_layer, dataset, type, id, variable=None, time_period=None
):
    layer_name = path.make_unique_layer_name(
        type, id, variable=variable, time_period=time_period
    )

    layer = geofile.load(layer_name)
    if layer is None:
        return

    mapnik_layers = layer.as_mapnik_layers()
    if mapnik_layers is None:
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

    low_left = None
    upper_right = None

    for mapnik_layer in mapnik_layers:
        layerproj = mapnik.Projection(mapnik_layer.srs)
        bbox = mapnik_layer.envelope()

        layer_low_left = layerproj.inverse(mapnik.Coord(bbox.minx, bbox.miny))
        layer_upper_right = layerproj.inverse(mapnik.Coord(bbox.maxx, bbox.maxy))

        if low_left is not None:
            low_left.x = min(low_left.x, layer_low_left.x)
            low_left.y = min(low_left.y, layer_low_left.y)
            upper_right.x = max(upper_right.x, layer_upper_right.x)
            upper_right.y = max(upper_right.y, layer_upper_right.y)
        else:
            low_left = layer_low_left
            upper_right = layer_upper_right

    projected_bbox = etree.Element("EX_GeographicBoundingBox")

    west_bound = etree.Element("westBoundLongitude")
    west_bound.text = str(low_left.x)
    projected_bbox.append(west_bound)

    east_bound = etree.Element("eastBoundLongitude")
    east_bound.text = str(upper_right.x)
    projected_bbox.append(east_bound)

    south_bound = etree.Element("southBoundLatitude")
    south_bound.text = str(low_left.y)
    projected_bbox.append(south_bound)

    north_bound = etree.Element("northBoundLatitude")
    north_bound.text = str(upper_right.y)
    projected_bbox.append(north_bound)

    sublayer_node.append(projected_bbox)

    for crs in current_app.config["WMS"]["ALLOWED_PROJECTIONS"]:
        bbox_node = etree.Element("BoundingBox")
        proj4 = projection.epsg_string_to_proj4(crs)
        proj_low_left = low_left.forward(mapnik.Projection(proj4))
        proj_upper_right = upper_right.forward(mapnik.Projection(proj4))
        bbox_node.set("minx", str(proj_low_left.x))
        bbox_node.set("maxx", str(proj_upper_right.x))
        bbox_node.set("miny", str(proj_low_left.y))
        bbox_node.set("maxy", str(proj_upper_right.y))
        bbox_node.set("CRS", crs)
        sublayer_node.append(bbox_node)

    parent_layer.append(sublayer_node)
