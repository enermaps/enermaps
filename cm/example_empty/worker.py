#!/usr/bin/env python3
import BaseCM.cm_base as cm_base
from BaseCM.cm_output import validate

app = cm_base.get_default_app()
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
def cm_empty(self, selection: dict, rasters: list, params: dict):
    ret = dict()
    ret["graphs"] = {}
    ret["geofiles"] = {}
    ret["values"] = {}
    return validate(ret)


if __name__ == "__main__":
    cm_base.start_app(app)
