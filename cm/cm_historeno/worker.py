#!/usr/bin/env python3

import requests
from BaseCM import cm_base as cm_base
from BaseCM.cm_output import validate

app = cm_base.get_default_app("cm-historeno")
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
        "typo": params["Typologie"],
        "generator": params["Type de chauffage"],
        "generatorYear": params["Année d'installation ou de remplacement du chauffage"],
        "emettors": params["Type d'émetteurs"],
        "regulation": params["Régulation du chauffage"],
        "tubeInsulH": params["Isolation des conduites de chauffage"],
        "tubeInsulW": params["Isolation des conduites d'ECS"],
        "solarThermal": params["Présence d'une installation solaire thermique"],
        "solarThermalAreaAuto": params[
            "Surface de capteurs solaires thermiques automatique"
        ],
        "solarThermalArea": params["Surface de capteurs solaires thermiques"],
        "devEff": params["Efficacité des appareils électriques"],
        "ventMeca": params["Présence d'une ventilation mécanique"],
        "elevator": params["Présence d'ascenseur(s)"],
        "solarPV": params["Présence d'une instalaltion solaire PV"],
        "pvAreaAuto": params["Surface PV automatique"],
        "pvArea": params["Surface PV"],
        "pvOri": params["Orientation PV"],
        "pvBattery": params["Présence de batteries de stockage"],
    }

    def post_parameters():
        """Post fake parameters."""
        url_endpoint = "https://historeno.heig-vd.ch/tool/calcPTF.php"
        try:
            resp = requests.post(url_endpoint, params=parameters)
            print(f"RESULTS: {resp.status_code}")
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
        "Example CM": "This CM is under development.",
    }
    return validate(ret)


if __name__ == "__main__":
    cm_base.start_app(app)
