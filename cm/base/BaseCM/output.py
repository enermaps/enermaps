from typing import Dict

from marshmallow import Schema, fields
from marshmallow_union import Union


class Value(Schema):
    value = fields.Number(required=True, allow_none=True)
    unit = fields.String(required=False)


class XYGraph(Schema):
    values = fields.List(
        fields.Tuple((fields.Number(), fields.Number())), required=True
    )
    unit = fields.Tuple((fields.Str(), fields.Str()), required=False)


class LineGraph(Schema):
    values = fields.List(fields.Number(), required=True)
    unit = fields.String(required=False)


class BarGraph(Schema):
    values = fields.List(fields.Tuple([fields.Str(), fields.Number()]), required=True)
    unit = fields.String(required=False)


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
