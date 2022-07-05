#!/usr/bin/env python3

import logging

import requests
import xmltodict
from BaseCM import cm_base as cm_base
from BaseCM.cm_output import validate

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
    def post_parameters():
        """Post on calculator to create task."""
        parameters = {
            "country": decoder.get("country").get(params["Pays"]),
            "canton": decoder.get("canton").get(params["Region"]),
            "altitude": params["Altitude"],
            "meteoParam": decoder.get("meteoParam").get(params["Météo"]),
            "context": decoder.get("context").get(params["Context"]),
            "polygon": "[[0,0],[0,10],[10,10],[10,0]]",
            "adjoining": "[0,0,0.5,0]",
            "typo": params["Typologie"],
            "year": params["Années de construction"],
            "category": params["Catégorie d'ouvrage"],
            "height": params["Hauteur du bâtiment"],
            "generator": decoder.get("generator").get(params["Type de chauffage"]),
            "generatorYear": params["Année d'installation du chauffage"],
            "emettors": decoder.get("emettors").get(params["Type d'émetteurs"]),
            "regulation": decoder.get("regulation").get(
                params["Régulation du chauffage"]
            ),
            "tubeInsulH": decoder.get("tubeInsulH").get(
                params["Isolation des conduites de chauffage"]
            ),
            "tubeInsulW": decoder.get("tubeInsulW").get(
                params["Isolation des conduites d'ECS"]
            ),
            "solarThermal": decoder.get("solarThermal").get(
                params["Présence d'une installation solaire thermique"]
            ),
            "solarThermalAreaAuto": decoder.get("solarThermalAreaAuto").get(
                params["Surface de capteurs solaires thermiques automatique"]
            ),
            "solarThermalArea": params["Surface de capteurs solaires thermiques"],
            "nbAppart": params["Nombre de logements"],
            "devEff": decoder.get("devEff").get(
                params["Efficacité des appareils électriques"]
            ),
            "ventMeca": decoder.get("ventMeca").get(
                params["Présence d'une ventilation mécanique"]
            ),
            "elevator": decoder.get("elevator").get(params["Présence d'ascenseur(s)"]),
            "solarPV": decoder.get("solarPV").get(
                params["Présence d'une instalaltion solaire PV"]
            ),
            "pvAreaAuto": decoder.get("pvAreaAuto").get(
                params["Surface PV automatique"]
            ),
            "pvArea": params["Surface PV"],
            "pvOri": params["Orientation PV"],
            "pvBattery": decoder.get("pvBattery").get(
                params["Présence de batteries de stockage"]
            ),
            "protectionGrade": params["Note de protection du patrimoine"],
            "heatingWood": decoder.get("heatingWood").get(
                params["Possibilité d'utiliser un chauffage au bois"]
            ),
            "heatingProbes": decoder.get("heatingProbes").get(
                params["Possibilité de mettre des sondes géothermiques"]
            ),
            "solarRoof": decoder.get("solarRoof").get(
                params["Possibilité de mettre du solaire en toiture"]
            ),
        }
        url_endpoint = "https://historeno.heig-vd.ch/tool/calcPTF.php"
        try:
            resp = requests.post(url_endpoint, data=parameters)
            logging.info(f"RESULTS: {resp.status_code}")
            # logging.info(f"URL: {resp.url}")
            # logging.info(f"CONTENT: {resp.content}")
            # pprint(f"CONTENT: {resp.content}")
            return resp
        except ConnectionError as error:
            logging.error("Error during the post of the file.")
            raise ConnectionError(error)

    res = post_parameters()
    ret = dict()
    ret["graphs"] = []
    ret["geofiles"] = {}
    values = xmltodict.parse(res.content)["project"]
    ret["values"] = {
        "Coût totaux [CHF]": values["bldOutput"]["Cost"],
        "Besoin de chauffage  [kWh]": values["bldOutput"]["Qh"],
        "Pertes par ventilation  [kWh]": values["bldOutput"]["Qv"],
        "Energie primaire non renouvelable totale [kWh]": values["bldOutput"]["NRE"],
    }
    ret["warnings"] = {}

    return validate(ret)


if __name__ == "__main__":
    cm_base.start_app(app)
