#!/usr/bin/env python3

import logging
from pprint import pprint

import requests
from BaseCM import cm_base as cm_base
from BaseCM.cm_output import validate

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
        "country": "CH",
        "canton": "VS",
        "altitude": 10.0,
        "meteoParam": "sud",
        "context": "urban",
        "polygon": "[[0,0],[0,10],[10,10],[10,0]]",
        "adjoining": "[0,0,0.5,0]",
        "gable": "[0,0,1,0]",
        "typo": params["Typologie"],
        "year": "1910",
        "category": 1,
        "height": 100.0,
        "generator": "genTypOil",  # TODO : transalte it --> params["Type de chauffage"],
        "generatorYear": params["Année d'installation ou de remplacement du chauffage"],
        "emettors": "emRadWall",  # TODO : transalte it --> params["Type d'émetteurs"],
        "regulation": 0,  # TODO : transalte it -->  params["Régulation du chauffage"],
        "tubeInsulH": "notInsulated",  # TODO : transalte it -->  params["Isolation des conduites de chauffage"],
        "tubeInsulW": "notInsulated",  # TODO : transalte it --> params["Isolation des conduites d'ECS"],
        "solarThermal": 1,  # TODO : transalte it --> params["Présence d'une installation solaire thermique"],
        "solarThermalAreaAuto": 0,  # TODO : transalte it -->  params["Surface de capteurs solaires thermiques automatique"],
        "solarThermalArea": 10,  # TODO : transalte it --> params["Surface de capteurs solaires thermiques"],
        "nbAppart": 0,
        "devEff": "best",  # TODO : transalte it --> params["Efficacité des appareils électriques"],
        "ventMeca": "none",  # TODO : transalte it --> params["Présence d'une ventilation mécanique"],
        "elevator": 0,  # TODO : transalte it -->  params["Présence d'ascenseur(s)"],
        "solarPV": 1,  # TODO : transalte it --> params["Présence d'une instalaltion solaire PV"],
        "pvAreaAuto": 0,  # TODO : transalte it --> params["Surface PV automatique"],
        "pvArea": 5.0,  # TODO : transalte it --> params["Surface PV"],
        "pvOri": 7.0,  # TODO : transalte it --> params["Orientation PV"],
        "pvBattery": 1,  # TODO : transalte it --> params["Présence de batteries de stockage"],
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
    ret["warnings"] = {
        "Example CM": f"Response: {res.content}.",
    }
    return validate(ret)


if __name__ == "__main__":
    cm_base.start_app(app)
