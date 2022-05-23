#!/usr/bin/env python3

import logging
from pprint import pprint

import requests
from BaseCM import cm_base as cm_base
from BaseCM.cm_output import validate
from lxml import etree

from form import decoder

app = cm_base.get_default_app("historeno")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()
wiki = "http://www.historeno.eu/"


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
    wiki=wiki,
)
def Module_Historeno(self, selection: dict, rasters: list, params: dict):
    parameters = {
        "country": decoder.get("coutry").get(params["Pays"]),
        "canton": decoder.get("canton").get(params["Region"]),
        "altitude": 10.0,
        "meteoParam": decoder.get("meteoParam").get(params["Pays"]),
        "context": decoder.get("context").get(params["Region"]),
        "polygon": "[[0,0],[0,10],[10,10],[10,0]]",
        "adjoining": "[0,0,0.5,0]",
        # "gable": "[0,0,1,0]",
        "typo": params["Typologie"],
        "year": "1910",
        "category": 1,
        "height": 100.0,
        "generator": decoder.get("generator").get(params["Region"]),
        "generatorYear": params["Année d'installation ou de remplacement du chauffage"],
        "emettors": decoder.get("emettors").get(params["Region"]),
        "regulation": decoder.get("regulation").get(params["Region"]),
        "tubeInsulH": decoder.get("tubeInsulH").get(params["Region"]),
        "tubeInsulW": decoder.get("tubeInsulW").get(params["Region"]),
        "solarThermal": decoder.get("solarThermal").get(params["Region"]),
        "solarThermalAreaAuto": decoder.get("solarThermalAreaAuto").get(
            params["Region"]
        ),
        "solarThermalArea": 10,
        "nbAppart": 0,
        "devEff": decoder.get("devEff").get(params["Region"]),
        "ventMeca": decoder.get("context").get(params["Region"]),
        "elevator": decoder.get("context").get(params["Region"]),
        "solarPV": decoder.get("context").get(params["Region"]),
        "pvAreaAuto": decoder.get("context").get(params["Region"]),
        "pvArea": 5.0,
        "pvOri": 7.0,
        "pvBattery": decoder.get("context").get(params["Region"]),
        "protectionGrade": 0,
        "heatingWood": decoder.get("context").get(params["Region"]),
        "heatingProbes": decoder.get("context").get(params["Region"]),
        "solarRoof": decoder.get("context").get(params["Region"]),
    }

    def post_parameters():
        """Post fake parameters."""
        url_endpoint = "https://historeno.heig-vd.ch/tool/calcPTF.php"
        try:
            resp = requests.post(url_endpoint, data=parameters)
            logging.info(f"RESULTS: {resp.status_code}")
            logging.info(f"URL: {resp.url}")
            logging.info(f"CONTENT: {resp.content}")
            pprint(f"CONTENT: {resp.content}")
            return resp
        except ConnectionError as error:
            print("Error during the post of the file.")
            raise ConnectionError(error)

    res = post_parameters()

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
    ret["values"] = {"Status code": res.status_code}

    xml_str = res.content
    root = etree.fromstring(xml_str)
    print(etree.tostring(root, pretty_print=True))
    ret["warnings"] = {
        "Example CM": f"Response: {etree.tostring(root, pretty_print=True)}.",
    }
    return validate(ret)


if __name__ == "__main__":
    cm_base.start_app(app)
