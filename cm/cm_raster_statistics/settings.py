import json
import logging
import os

import requests

API_URL = os.environ.get("API_URL", "https://lab.idiap.ch/enermaps/api")
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def list_input_layers():
    output_file = os.path.join(CURRENT_DIR, "input_layers.json")
    response = requests.get(f"{API_URL}/datasets/full/")
    layers = list()
    for dataset in response.json():
        temp = dict()
        if dataset["is_raster"]:
            temp["dataset"] = dataset["ds_id"]
            if dataset["info"]["variables"]:
                temp["variables"] = dataset["info"]["variables"]
            layers.append(temp)
        del temp
    if os.path.isfile(output_file):
        os.remove(output_file)
    with open(output_file, "w") as outfile:
        json.dump(layers, outfile)
    if not os.path.exists(output_file):
        raise FileNotFoundError(
            f"The file has not been created and is mandatory. : {output_file}"
        )
    logging.info("The input_layers.json file has been created correctly.")


if __name__ == "__main__":
    list_input_layers()
