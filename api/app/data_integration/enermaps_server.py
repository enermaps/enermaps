#!/usr/bin/python

import inspect
import io
import os
import sys
import json

import requests
from werkzeug.datastructures import FileStorage

from app.data_integration.data_config import DATASETS_DIC
#from data_config import DATASETS_DIC

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

#API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYXBpX3VzZXIifQ.i34NXwqCFDV84ZKjZ0b7r4OmHOeRkONEEKARQSbNL00"

SERVER_URL = "https://lab.idiap.ch/enermaps/api/"
SERVER_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYXBpX3VzZXIifQ.gzl3uCe1OdCjf3feliREDJFfNkMTiDkVFcVDrCNlpBU"

#TODO
RASTER_SERVER_URL = "https://lab.idiap.ch/enermaps/raster/15/2015-01-01_u10_band1_3035.tif"


def get_datasets_ids():
    return [2]


def get_dataset(dataset_id=0):
    """
    Fetch a geojson dataset from the enermaps server with a given Id.
    """
    url = SERVER_URL + "rpc/enermaps_query_geojson"

    # Get the dataset parameters
    params = None
    layer_type = None
    for key, value in DATASETS_DIC.items():
        if value["id"] == dataset_id:
            params = value["json_params"]
            layer_type = value["layer_type"]

    if (params is not None) and (layer_type == "vector"):
        print("Fetching json dataset " + str(dataset_id))
        try:
            with requests.post(
                url,
                headers={"Authorization": "Bearer {}".format(SERVER_API_KEY)},
                json=params
            ) as resp:
                # print(resp.json())
                # with open(str(dataset_id) + ".geojson", "w") as f:
                #     json_data = json.dumps(resp.json(), indent=4, sort_keys=True)
                #     f.write(json_data)
                resp_data = io.BytesIO(resp.content)

            print(resp_data)
            filename = str(dataset_id) + ".geojson"
            content_type = "application/geo+json"
            file_upload = FileStorage(resp_data, filename, content_type=content_type)    
            print(file_upload)
            return file_upload
        except ConnectionError:
            print("Coucou l'exception geojson", flush=True)

    if (params is not None) and (layer_type == "raster"):
        print("Fetching raster dataset " + str(dataset_id))

        tif_query = {
            "service": "WMS",
            "version": "1.1.0",
            "request": "GetMap",
            "layers": "hotmaps:gfa_tot_curr_density",
            "styles": "",
            "bbox": "944000.0,938000.0,6528000.0,5414000.0",
            "width": 768,
            "height": 615,
            "srs": "EPSG:3035",
            "format": "image/geotiff",
        }

        try:
            with requests.get(RASTER_SERVER_URL, stream=True) as resp:
                resp_data = io.BytesIO(resp.content)

            filename = str(dataset_id) + ".tiff"
            content_type = "image/tiff"
            file_upload = FileStorage(resp_data, filename, content_type=content_type)
            return file_upload
        except ConnectionError:
            print("coucou l'exception raster", flush=True)



if __name__ == "__main__":
    get_dataset(2)