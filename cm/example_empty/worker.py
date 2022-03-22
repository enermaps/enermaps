#!/usr/bin/env python3

from BaseCM import cm_base as cm_base
from BaseCM.cm_output import validate

app = cm_base.get_default_app("empty")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()
wiki = "https://enermaps-wiki.herokuapp.com/en/Home"


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
    wiki=wiki,
)
def cm_empty(self, selection: dict, rasters: list, params: dict):
    ret = dict()
    ret["graphs"] = [
        {
            "title": {"type": "bar", "values": [(f"val {i}", i) for i in range(10)]},
        },
        {
            "title2": {
                "type": "xy",
                "values": [(f"val {i*2}", i * 2) for i in range(10)],
            },
        },
    ]
    ret["geofiles"] = {}
    ret["values"] = {"input": params["my_input"]}
    ret["warnings"] = {
        "Example CM": "This CM just returns the input.",
    }
    return validate(ret)


if __name__ == "__main__":
    cm_base.start_app(app)
