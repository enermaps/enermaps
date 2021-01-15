import os
from typing import Dict

import requests
from marshmallow import Schema, fields
from marshmallow_union import Union


class Value(Schema):
    value = fields.Number(required=True, allow_none=True)
    unit = fields.String(required=True)


class XYGraph(Schema):
    values = fields.List(
        fields.Tuple((fields.Number(), fields.Number())), required=True
    )
    unit = fields.Tuple((fields.Str(), fields.Str()), required=False)

    class Meta:
        include = {"type": fields.Constant("xy", required=True)}


class LineGraph(Schema):
    values = fields.List(fields.Number(), required=True)
    unit = fields.String(required=False)

    class Meta:
        include = {"type": fields.Constant("line", required=True)}


class BarGraph(Schema):
    values = fields.List(fields.Tuple([fields.Str(), fields.Number()]), required=True)
    unit = fields.String(required=False)

    class Meta:
        include = {"type": fields.Constant("bar", required=True)}


class CMOutput(Schema):
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
    output_schema = CMOutput()
    out = output_schema.load(data=output)
    return out


# get the api url
API_URL = os.environ.get("API_URL")


def output_raster(raster_name, raster_fd):
    """Add a raster to the api"""
    files = {"file": (raster_name, raster_fd, "image/tiff")}
    resp = requests.post(API_URL + "api/geofile/", files=files)
    return resp.ok
