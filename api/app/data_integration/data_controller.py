import io
import os
import requests
from werkzeug.datastructures import FileStorage
from app.common import db
from app.models.geofile import create, list_layers

from app.data_integration import enermaps_db
from app.data_integration import enermaps_server

def init_enermaps_datasets():

    # These datasets are tiled raster datasets (needing input coordinates)
    datasets_to_exclude = [21, 24, 33, 35]

    # Get the ids of all the datasets that are in the eneramps DB
    print("Datasets ids -------------------------")
    datasets_ids = enermaps_server.get_datasets_ids()
    print(datasets_ids)

    for id in datasets_ids:
        if id not in datasets_to_exclude:
            data = enermaps_server.get_dataset(id)




# Hotmaps datasets ---------------------------------------------------------------------------

def fetch_dataset(base_url, get_parameters, filename, content_type):
    """Get a single zip dataset and import it into enermaps."""
    existing_layers_name = [layer.name for layer in list_layers()]
    if filename in existing_layers_name:
        print("Not fetching {}, we already have it locally".format(filename))
        return
    print("Fetching " + filename)
    with requests.get(base_url, params=get_parameters, stream=True) as resp:
        resp_data = io.BytesIO(resp.content)
    file_upload = FileStorage(resp_data, filename, content_type=content_type)
    create(file_upload)


def init_hotmaps_datasets():
    """If the dataset was found to be empty, initialize the datasets for
    the selection of:
    * NUTS(0|1|2|3)
    * LAU

    Currently, we fetch the dataset from hotmaps.eu
    """
    print("Ensure we have the initial set of dataset")
    base_url = "https://geoserver.hotmaps.eu/geoserver/hotmaps/ows"
    base_query_params = {
        "service": "WFS",
        "version": "1.0.0",
        "request": "GetFeature",
        "outputFormat": "SHAPE-ZIP",
    }
    nuts_query = {**base_query_params, **{"typeName": "hotmaps:nuts"}}
    cql_filter = "stat_levl_='{!s}' AND year='2013-01-01'"
    lau_query = {**base_query_params, **{"typeName": "hotmaps:tbl_lau1_2"}}
    for i in range(4):
        nuts_query["CQL_FILTER"] = cql_filter.format(i)
        filename = "nuts{!s}.zip".format(i)
        fetch_dataset(base_url, nuts_query, filename, "application/zip")

    filename = "lau.zip"
    fetch_dataset(base_url, lau_query, filename, "application/zip")

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
    filename = "gfa_tot_curr_density.tiff"
    fetch_dataset(base_url, tif_query, filename, "image/tiff")
