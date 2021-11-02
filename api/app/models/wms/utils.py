"""Utility functions for the Web Map Service (WMS)"""

import urllib
from collections import namedtuple

import mapnik
from flask import abort, current_app

MIME_TO_MAPNIK = {"image/png": "png", "image/jpg": "jpeg"}


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
    elif srs:
        return srs.lower()
    else:
        return crs.lower()


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
