#!/usr/bin/env python3
import BaseCM.cm_base as cm_base

from geojson import process

app = cm_base.get_default_app()
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
def new_cm(self, file: str, params: dict):
    """New cm to test the integration work flow"""
    geofile_output = process(file)
    return geofile_output


if __name__ == "__main__":
    cm_base.start_app(app)
