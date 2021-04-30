import logging
import os
from typing import Dict

import requests
from marshmallow import Schema, fields
from marshmallow_union import Union
from requests.exceptions import ConnectionError

API_URL = os.environ.get("API_URL")


class Value(Schema):
    """Class that defines the value schema."""

    value = fields.Number(required=True, allow_none=True)
    unit = fields.String(required=True)


class XYGraph(Schema):
    """Class that defines the x/y graph value schema."""

    values = fields.List(
        fields.Tuple((fields.Number(), fields.Number())), required=True
    )
    unit = fields.Tuple((fields.Str(), fields.Str()), required=False)

    class Meta:
        include = {"type": fields.Constant("xy", required=True)}


class LineGraph(Schema):
    """Class that defines the x/y graph value schema."""

    values = fields.List(fields.Number(), required=True)
    unit = fields.String(required=False)

    class Meta:
        include = {"type": fields.Constant("line", required=True)}


class BarGraph(Schema):
    """Class that defines the bar graph value schema."""

    values = fields.List(fields.Tuple([fields.Str(), fields.Number()]), required=True)
    unit = fields.String(required=False)

    class Meta:
        include = {"type": fields.Constant("bar", required=True)}


class CMOutput(Schema):
    """Class that defines the CM output value schema."""

    graphs = fields.Dict(
        keys=fields.Str(),
        values=Union(
            [
                fields.Nested(BarGraph()),
                fields.Nested(LineGraph()),
                fields.Nested(XYGraph()),
            ]
        ),
        required=True,
    )
    geofiles = fields.Dict(keys=fields.Str(), values=fields.Str(), required=True)
    values = fields.Dict(
        keys=fields.Str(),
        values=Union(
            [fields.Number(allow_none=True), fields.Nested(Value)], allow_none=True
        ),
        required=True,
    )


def validate(output: Dict) -> Dict:
    """Validate the output of the CM based on the CM output schema."""
    output_schema = CMOutput()
    # validates and deserializes an input dictionary to an application-level
    # data structure
    return output_schema.load(data=output)


def output_raster(raster_name, raster_fd):
    """Add a raster to the api."""
    files = {"file": (raster_name, raster_fd, "image/tiff")}
    try:
        resp = requests.post(API_URL + "/geofile/", files=files)
    except ConnectionError:
        logging.error("Error during the post of the file.")
    return resp.status_code
