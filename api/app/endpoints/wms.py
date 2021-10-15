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

import mapnik
from flask import Response, abort, request
from flask_restx import Namespace, Resource

from app.models import geofile
from app.models.wms import utils
from app.models.wms.capabilities import get_capabilities
from app.models.wms.map import delete_image_folders, get_mapnik_map

api = Namespace("wms", "WMS compatible endpoint")


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
        return Response(get_capabilities(), mimetype="text/xml")

    def get_map(self, normalized_args):
        """Return the map."""
        mapnik_format, mime_format = utils.parse_format(normalized_args)
        size = utils.parse_size(normalized_args)

        mp = get_mapnik_map(normalized_args)
        if mp is None:
            abort(404)

        mp.zoom_to_box(utils.parse_envelope(normalized_args))

        image = mapnik.Image(size.width, size.height)
        mapnik.render(mp, image)

        delete_image_folders(mp)

        return Response(image.tostring(mapnik_format), mimetype=mime_format)

    def get_feature_info(self, normalized_args):
        """Implement the GetFeatureInfo entrypoint for the WMS endpoint"""
        # TODO: fix this to output text, xml and json !
        # currently, only support application/json as mimetype

        if normalized_args["info_format"] != "application/json":
            abort(400, "this endpoint doesn't support non json return value")

        mp = get_mapnik_map(normalized_args)
        if mp is None:
            abort(404)

        mp.zoom_to_box(utils.parse_envelope(normalized_args))

        raw_query_layers = normalized_args.get("query_layers", "")
        query_layers = utils.parse_list(raw_query_layers)
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

            position = utils.parse_position(normalized_args)

            # carefull here, this is a WMS 1.1.1 query maybe ?
            featureset = mp.query_map_point(layerindex, position.x, position.y)
            for feature in featureset:
                features["features"].append(json.loads(feature.to_geojson()))

        return features
