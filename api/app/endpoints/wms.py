"""
The Web Map Service (WMS) provides a simple HTTP interface for requesting
geo-registered map images from one or more distributed geospatial databases.
(source : https://www.ogc.org/standards/wms#schemas)

The three operations defined for a WMS are :
* GetCapabilities (to obtain service metadata) [MANDATORY],
* GetMap (to obtain the map) [MANDATORY],
* and GetFeatureInfo [OPTIONAL].

For more information about the WMS, see https://portal.ogc.org/files/?artifact_id=14416.
"""
import json
import os
import urllib
from collections import namedtuple

import mapnik
from flask import Response, abort, current_app, request
from flask_restx import Namespace, Resource
from lxml import etree  # nosec

from app.common import projection as projection
from app.common import xml as xml
from app.data_integration import data_endpoints
from app.models import geofile as geofile

MIME_TO_MAPNIK = {"image/png": "png", "image/jpg": "jpg"}

api = Namespace("wms", "WMS compatible endpoint")
current_file_dir = os.path.dirname(os.path.abspath(__file__))


def parse_envelope(params):
    """Parse the map and return the bounding box."""
    raw_extremas = params["bbox"].split(",")
    if len(raw_extremas) != 4:
        abort(400, "bounding box need four extremas")
    try:
        minx, miny, maxx, maxy = [float(extrema) for extrema in raw_extremas]
    except ValueError:
        abort(
            400,
            "Excepted the bounding box to be a comma separated "
            "list of floating point numbers",
        )
    if (minx == maxx) or (miny == maxy):
        abort(400, "envelope area shouldn't be 0")
    bbox = mapnik.Box2d(minx, miny, maxx, maxy)
    return bbox


def parse_layers(params):
    """Parse the map and return the list of layers."""
    try:
        raw_layers = params["layers"]
    except KeyError:
        abort(400, "Parameter layers was not found")
    return parse_list(raw_layers)


def parse_list(raw_string):
    """Read a comma separated list of quoted string, this is used for the list of layer
    and the list of style in the wms.
    """
    raw_list = raw_string.split(",")
    parsed_list = [urllib.parse.unquote(el) for el in raw_list]
    return parsed_list


def parse_projection(params):
    """Parse the map and return the projection."""
    srs = params.get("srs")
    crs = params.get("crs")
    if not (srs or crs):
        abort(400, "Parameter srs nor crs was not found")
    return srs.lower()


Size = namedtuple("Size", ("width", "height"))


def parse_size(params) -> Size:
    """Parse the map, check if it doesn't exceed the maximal size allowed,
    and then return the size of the map.
    """
    try:
        height = int(params["height"])
        width = int(params["width"])
    except (KeyError, ValueError):
        abort(
            400,
            "Size parameter (height or width) couldn't be extracted "
            "correctly from the list of parameters ",
        )
    if (height * width) > current_app.config["WMS"]["MAX_SIZE"]:
        abort(400, "Total size is bigger than the maximal allowed size")
    return Size(width=width, height=height)


Position = namedtuple("Position", ("x", "y"))


def parse_position(params) -> Position:
    """Parse the map and return position parameter (x and y)."""
    try:
        x = float(params["x"])
        y = float(params["y"])
    except (ValueError, KeyError):
        abort(
            400,
            "Position parameter (x or y) couldn't be extracted "
            "correctly from the list of parameters",
        )
    return Position(x=x, y=y)


def parse_format(params):
    """Parse the map and return format.
    Check that it is in the allowed list of format.
    """
    try:
        mime_format = params["format"]
    except KeyError:
        abort(400, "Couldn't find the format parameters")
    allowed_outputs = current_app.config["WMS"]["GETMAP"]["ALLOWED_OUTPUTS"]
    if mime_format not in allowed_outputs:
        raise Exception()
    try:
        mapnik_format = MIME_TO_MAPNIK[mime_format]
    except ValueError:
        abort(400, "return format is not supported")
    return mapnik_format, mime_format


@api.route("")
# @api.reponse(400, "Couldn't find the requested method")
class WMS(Resource):
    def get(self):
        normalized_args = {k.lower(): v for k, v in request.args.items()}
        service = normalized_args.get("service")
        if service != "WMS":
            normalized_args["service"] = "WMS"
        request_name = normalized_args.get("request")
        if request_name == "GetMap":
            return self.get_map(normalized_args)
        if request_name == "GetCapabilities":
            return self.get_capabilities(normalized_args)
        if request_name == "GetFeatureInfo":
            return self.get_feature_info(normalized_args)
        return abort(
            400,
            "Couldn't find the requested method {}, "
            "request parameter needs to be set".format(request_name),
        )

    def get_capabilities(self, _):
        """Return an xml description of the capabilities of the current wms
        set of endpoints.

        This method starts with a preexisting xml template parses it then
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
        layers = geofile.list_layers()
        for layer in layers:
            layer_node = etree.Element("Layer")
            layer_node.set("queryable", "1" if layer.is_queryable else "0")
            # all layers presented by the api are opaque
            layer_node.set("opaque", "0")
            name_node = etree.Element("Name")
            name_node.text = layer.name
            layer_node.append(name_node)
            title_node = etree.Element("Title")
            title_node.text = "This is layer {}".format(layer.name)
            layer_node.append(title_node)
            abstract = etree.Element("Abstract")
            layer_node.append(abstract)
            keyword_list = etree.Element("KeywordList")
            layer_node.append(keyword_list)

            for crs in current_app.config["WMS"]["ALLOWED_PROJECTIONS"]:
                crs_node = etree.Element("CRS")
                crs_node.text = crs.upper()
                layer_node.append(crs_node)

            mapnik_layer = layer.as_mapnik_layer()
            layerproj = mapnik.Projection(mapnik_layer.srs)
            bbox = mapnik_layer.envelope()
            low_left = layerproj.inverse(mapnik.Coord(bbox.minx, bbox.miny))
            upper_right = layerproj.inverse(mapnik.Coord(bbox.maxx, bbox.maxy))
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
            layer_node.append(projected_bbox)

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
                layer_node.append(bbox_node)

            root_layer.append(layer_node)

        # TODO: add a reference to a legend and have an endpoint for it

        etree.indent(root, space="    ")
        return Response(etree.tostring(root, pretty_print=True), mimetype="text/xml")

    def _get_map(self, normalized_args):
        """Return the Mapnik object (with hardcoded symbology/rule)."""
        # miss:
        # bgcolor
        # exceptions
        projection = parse_projection(normalized_args)
        # validate projection
        size = parse_size(normalized_args)

        mp = mapnik.Map(size.width, size.height, "+init=" + projection)

        s = mapnik.Style()
        r = mapnik.Rule()

        r.symbols.append(mapnik.RasterSymbolizer())
        s.rules.append(r)

        r.symbols.append(mapnik.PointSymbolizer())
        s.rules.append(r)

        layer_name = normalized_args.get("layers", "")

        # setup the "legends" rules
        if layer_name[0:2].isdigit():
            layer_id = int(layer_name[0:2])

            # Get the variable used to color the polygons and its min/max values
            layer_variable = data_endpoints.get_legend_variable(layer_id)
            if layer_variable is not None:

                # Layer style is never None, if there is no custom style defined a
                # default style is returned
                layer_style = data_endpoints.get_legend_style(layer_id)
                nb_of_colors = len(layer_style)

                # Create one polygon symbolizer per color
                polygons = []
                for color, min_threshold, max_threshold in layer_style:
                    polygons.append(mapnik.PolygonSymbolizer())
                    polygons[-1].fill = mapnik.Color(*color)
                    polygons[-1].fill_opacity = 0.5

                rules = []
                for n in range(nb_of_colors):
                    if n == 0:
                        expression = f"[legend] < {layer_style[n][2]}"
                    elif n == nb_of_colors:
                        expression = f"[legend] >= {layer_style[n][1]}"
                    else:
                        expression = f"[legend] < {layer_style[n][2]} and [legend] > {layer_style[n][1]}"

                    rules.append(mapnik.Rule())
                    rules[-1].filter = mapnik.Expression(expression)
                    rules[-1].symbols.append(polygons[n])
                    s.rules.append(rules[-1])

            else:
                # If there is no variable defined for coloring the polygons,
                # put the same black on all polygons
                polygon_symbolizer = mapnik.PolygonSymbolizer()
                polygon_symbolizer.fill = mapnik.Color("black")
                polygon_symbolizer.fill_opacity = 0.3
                r.symbols.append(polygon_symbolizer)

        # add the black polygons contours
        line_symbolizer = mapnik.LineSymbolizer()
        line_symbolizer.stroke = mapnik.Color("black")
        line_symbolizer.stroke_width = 1.0
        r.symbols.append(line_symbolizer)
        s.rules.append(r)

        style_name = "My Style"
        mp.append_style(style_name, s)

        layer_names = parse_layers(normalized_args)
        for layer_name in layer_names:
            try:
                layer = geofile.load(layer_name)
            except FileNotFoundError as e:
                abort(404, e.strerror)
            mapnik_layer = layer.as_mapnik_layer()
            mapnik_layer.styles.append(style_name)
            mp.layers.append(mapnik_layer)
        return mp

    def get_map(self, normalized_args):
        """Return the map."""
        mapnik_format, mime_format = parse_format(normalized_args)
        size = parse_size(normalized_args)
        mp = self._get_map(normalized_args)
        mp.zoom_to_box(parse_envelope(normalized_args))
        image = mapnik.Image(size.width, size.height)
        mapnik.render(mp, image)
        return Response(image.tostring(mapnik_format), mimetype=mime_format)

    def get_feature_info(self, normalized_args):
        """Implement the GetFeatureInfo entrypoint for the WMS endpoint"""
        # TODO: fix this to output text, xml and json !
        # currently, only support application/json as mimetype
        if normalized_args["info_format"] != "application/json":
            abort(400, "this endpoint doesn't support non json return value")
        mp = self._get_map(normalized_args)
        mp.zoom_to_box(parse_envelope(normalized_args))
        raw_query_layers = normalized_args.get("query_layers", "")
        query_layers = parse_list(raw_query_layers)
        if set(query_layers) != {layer.name for layer in mp.layers}:
            abort(400, "Requested layer didnt match the query_layers " "parameter")
        features = {"features": []}
        for layerindex, mapnick_layer in enumerate(mp.layers):
            layer_name = mapnick_layer.name
            layer = geofile.load(layer_name)
            if not layer.is_queryable:
                abort(
                    400, "Requested query layer {} is not queryable.".format(layer.name)
                )
            mapnick_layer.queryable = True
            position = parse_position(normalized_args)
            # carefull here, this is a WMS 1.1.1 query maybe ?
            featureset = mp.query_map_point(layerindex, position.x, position.y)
            for feature in featureset:
                features["features"].append(json.loads(feature.to_geojson()))
        return features
