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

from flask import Response, abort, request
from flask_restx import Namespace, Resource

from app.common import path
from app.models.wms import utils
from app.models.wms.capabilities import get_capabilities
from app.models.wms.map import get_map_image, get_mapnik_map_for_feature_info

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
        capabilities = get_capabilities()
        if capabilities is None:
            abort(404)

        return Response(capabilities, mimetype="text/xml")

    def get_map(self, normalized_args):
        """Return the map."""
        image = get_map_image(normalized_args)
        if image is None:
            abort(404)

        mapnik_format, mime_format = utils.parse_format(normalized_args)
        return Response(image.tostring(mapnik_format), mimetype=mime_format)

    def get_feature_info(self, normalized_args):
        """Implement the GetFeatureInfo entrypoint for the WMS endpoint"""
        # TODO: fix this to output text, xml and json !
        # currently, only support application/json as mimetype
        if normalized_args["info_format"] != "application/json":
            abort(400, "this endpoint doesn't support non json return value")

        mp = get_mapnik_map_for_feature_info(normalized_args)
        if mp is None:
            abort(404)

        mp.zoom_to_box(utils.parse_envelope(normalized_args))

        raw_query_layers = normalized_args.get("query_layers", "")
        query_layers = utils.parse_list(raw_query_layers)
        if set(query_layers) != {layer.name for layer in mp.layers}:
            abort(400, "Requested layer didnt match the query_layers parameter")

        features = {"features": []}
        for layerindex, mapnick_layer in enumerate(mp.layers):
            mapnick_layer.queryable = True

            (type, _, variable, _, _) = path.parse_unique_layer_name(mapnick_layer.name)

            position = utils.parse_position(normalized_args)

            layer_features = []
            variable_found = None

            featureset = mp.query_map_point(layerindex, position.x, position.y)
            for feature in featureset:
                geojson = json.loads(feature.to_geojson())
                layer_features.append(geojson)

                if (type == path.VECTOR) and not (variable_found):
                    variable_found = ("properties" in geojson) and (
                        f"__variable__{variable}" in geojson["properties"]
                    )

            if (type == path.AREA) or variable_found:
                features["features"].extend(layer_features)

        return features
